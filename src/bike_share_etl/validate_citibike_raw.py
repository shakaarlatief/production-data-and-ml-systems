import argparse
import math
import os
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"

ALLOWED_RIDEABLE_TYPES = {
    "classic_bike",
    "electric_bike",
}

ALLOWED_MEMBER_TYPES = {
    "member",
    "casual",
}

LONG_TRIP_THRESHOLD_SECONDS = 24 * 60 * 60

VALID_COPY_SQL = """
    COPY staging.citibike_trip_valid (
        file_id,
        source_row_number,
        ride_id,
        rideable_type,
        started_at,
        ended_at,
        duration_seconds,
        start_station_name,
        start_station_id,
        end_station_name,
        reported_end_station_id,
        resolved_end_station_id,
        end_station_id_resolution_method,
        start_lat,
        start_lng,
        end_lat,
        end_lng,
        member_casual,
        is_long_trip,
        has_missing_end_station,
        has_missing_end_coordinates
    )
    FROM STDIN
"""

REJECTED_COPY_SQL = """
    COPY staging.citibike_trip_rejected (
        file_id,
        source_row_number,
        ride_id,
        rejection_reasons
    )
    FROM STDIN
"""


def parse_arguments() -> argparse.Namespace:
    """Parse the source file identifier supplied on the command line."""
    parser = argparse.ArgumentParser(
        description=(
            "Validate one raw Citi Bike file and load accepted and rejected "
            "records into the staging schema."
        )
    )
    parser.add_argument(
        "--file-id",
        type=int,
        required=True,
        help="The source.citibike_file.file_id value to validate.",
    )
    return parser.parse_args()


def get_connection_parameters() -> dict[str, str]:
    """Load PostgreSQL connection parameters from the local environment file."""
    if not ENV_FILE.exists():
        raise FileNotFoundError(
            f"Environment configuration file not found: {ENV_FILE}"
        )

    load_dotenv(dotenv_path=ENV_FILE)

    return {
        "host": os.environ["DB_HOST"],
        "port": os.environ["DB_PORT"],
        "dbname": os.environ["DB_NAME"],
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
    }


def normalize_text(value: str | None) -> str | None:
    """Strip surrounding whitespace and convert blank text to None."""
    if value is None:
        return None

    normalized_value = value.strip()

    if normalized_value == "":
        return None

    return normalized_value


def parse_required_timestamp(
    value: str | None,
    column_name: str,
    rejection_reasons: list[str],
) -> datetime | None:
    """Parse a required timestamp and record a reason when parsing fails."""
    normalized_value = normalize_text(value)
    reason_suffix = column_name.upper()

    if normalized_value is None:
        rejection_reasons.append(f"MISSING_{reason_suffix}")
        return None

    try:
        return datetime.fromisoformat(normalized_value)
    except ValueError:
        rejection_reasons.append(f"INVALID_{reason_suffix}")
        return None


def parse_coordinate(
    value: str | None,
    column_name: str,
    minimum: float,
    maximum: float,
    required: bool,
    rejection_reasons: list[str],
) -> float | None:
    """Parse one coordinate and validate finiteness and geographic range."""
    normalized_value = normalize_text(value)
    reason_suffix = column_name.upper()

    if normalized_value is None:
        if required:
            rejection_reasons.append(f"MISSING_{reason_suffix}")
        return None

    try:
        coordinate = float(normalized_value)
    except ValueError:
        rejection_reasons.append(f"INVALID_{reason_suffix}")
        return None

    if not math.isfinite(coordinate):
        rejection_reasons.append(f"NONFINITE_{reason_suffix}")
        return None

    if not minimum <= coordinate <= maximum:
        rejection_reasons.append(f"OUT_OF_RANGE_{reason_suffix}")
        return None

    return coordinate


def build_station_name_to_ids(
    cursor: psycopg.Cursor[dict[str, Any]],
) -> dict[str, set[str]]:
    """Build observed station-name to station-ID relationships from raw data."""
    station_name_to_ids: defaultdict[str, set[str]] = defaultdict(set)

    cursor.execute(
        """
        SELECT
            start_station_name,
            start_station_id,
            end_station_name,
            end_station_id
        FROM source.citibike_trip_raw;
        """
    )

    for row in cursor:
        for prefix in ("start", "end"):
            station_name = normalize_text(row[f"{prefix}_station_name"])
            station_id = normalize_text(row[f"{prefix}_station_id"])

            if station_name is not None and station_id is not None:
                station_name_to_ids[station_name].add(station_id)

    return dict(station_name_to_ids)


def fetch_existing_valid_ride_ids(
    cursor: psycopg.Cursor[dict[str, Any]],
    file_id: int,
) -> set[str]:
    """Return ride identifiers already accepted from other source files."""
    cursor.execute(
        """
        SELECT ride_id
        FROM staging.citibike_trip_valid
        WHERE file_id <> %s;
        """,
        (file_id,),
    )

    return {row["ride_id"] for row in cursor}


def fetch_manifest_record(
    cursor: psycopg.Cursor[dict[str, Any]],
    file_id: int,
) -> dict[str, Any]:
    """Return the manifest record for the requested source file."""
    cursor.execute(
        """
        SELECT
            file_id,
            source_filename,
            source_sha256,
            source_row_count,
            loaded_at
        FROM source.citibike_file
        WHERE file_id = %s;
        """,
        (file_id,),
    )

    manifest_record = cursor.fetchone()

    if manifest_record is None:
        raise ValueError(
            f"No source.citibike_file record exists for file_id={file_id}."
        )

    return manifest_record


def fetch_raw_rows(
    cursor: psycopg.Cursor[dict[str, Any]],
    file_id: int,
) -> list[dict[str, Any]]:
    """Return raw source rows for one file in original source-row order."""
    cursor.execute(
        """
        SELECT
            file_id,
            source_row_number,
            ride_id,
            rideable_type,
            started_at,
            ended_at,
            start_station_name,
            start_station_id,
            end_station_name,
            end_station_id,
            start_lat,
            start_lng,
            end_lat,
            end_lng,
            member_casual
        FROM source.citibike_trip_raw
        WHERE file_id = %s
        ORDER BY source_row_number;
        """,
        (file_id,),
    )

    return list(cursor.fetchall())


def validate_raw_row(
    raw_row: dict[str, Any],
    station_name_to_ids: dict[str, set[str]],
    seen_valid_ride_ids: set[str],
) -> tuple[
    tuple[Any, ...] | None,
    tuple[str, ...],
    tuple[str, ...],
]:
    """Validate one raw row and return a valid row or rejection reasons."""
    rejection_reasons: list[str] = []
    quality_flags: list[str] = []

    file_id = raw_row["file_id"]
    source_row_number = raw_row["source_row_number"]

    ride_id = normalize_text(raw_row["ride_id"])

    if ride_id is None:
        rejection_reasons.append("MISSING_RIDE_ID")
    elif ride_id in seen_valid_ride_ids:
        rejection_reasons.append("DUPLICATE_RIDE_ID")

    rideable_type = normalize_text(raw_row["rideable_type"])

    if rideable_type is None:
        rejection_reasons.append("MISSING_RIDEABLE_TYPE")
    elif rideable_type not in ALLOWED_RIDEABLE_TYPES:
        rejection_reasons.append("UNKNOWN_RIDEABLE_TYPE")

    member_casual = normalize_text(raw_row["member_casual"])

    if member_casual is None:
        rejection_reasons.append("MISSING_MEMBER_TYPE")
    elif member_casual not in ALLOWED_MEMBER_TYPES:
        rejection_reasons.append("UNKNOWN_MEMBER_TYPE")

    started_at = parse_required_timestamp(
        raw_row["started_at"],
        "started_at",
        rejection_reasons,
    )
    ended_at = parse_required_timestamp(
        raw_row["ended_at"],
        "ended_at",
        rejection_reasons,
    )

    duration_seconds: float | None = None

    if started_at is not None and ended_at is not None:
        duration_seconds = (ended_at - started_at).total_seconds()

        if duration_seconds <= 0:
            rejection_reasons.append("NONPOSITIVE_DURATION")

    start_station_name = normalize_text(raw_row["start_station_name"])
    start_station_id = normalize_text(raw_row["start_station_id"])

    if start_station_name is None:
        rejection_reasons.append("MISSING_START_STATION_NAME")

    if start_station_id is None:
        rejection_reasons.append("MISSING_START_STATION_ID")

    end_station_name = normalize_text(raw_row["end_station_name"])
    reported_end_station_id = normalize_text(raw_row["end_station_id"])

    if reported_end_station_id is not None:
        resolved_end_station_id = reported_end_station_id
        end_station_id_resolution_method = "source"
    elif end_station_name is not None:
        observed_station_ids = station_name_to_ids.get(
            end_station_name,
            set(),
        )

        if len(observed_station_ids) == 1:
            resolved_end_station_id = next(iter(observed_station_ids))
            end_station_id_resolution_method = (
                "inferred_from_station_name"
            )
            quality_flags.append("END_STATION_ID_INFERRED")
        elif len(observed_station_ids) > 1:
            resolved_end_station_id = None
            end_station_id_resolution_method = "ambiguous_station_name"
            quality_flags.append("END_STATION_ID_AMBIGUOUS")
        else:
            resolved_end_station_id = None
            end_station_id_resolution_method = "unavailable"
    else:
        resolved_end_station_id = None
        end_station_id_resolution_method = "unavailable"

    has_missing_end_station = resolved_end_station_id is None

    if has_missing_end_station:
        quality_flags.append("MISSING_END_STATION")

    start_lat = parse_coordinate(
        raw_row["start_lat"],
        "start_lat",
        -90,
        90,
        True,
        rejection_reasons,
    )
    start_lng = parse_coordinate(
        raw_row["start_lng"],
        "start_lng",
        -180,
        180,
        True,
        rejection_reasons,
    )

    end_lat_text = normalize_text(raw_row["end_lat"])
    end_lng_text = normalize_text(raw_row["end_lng"])

    if (end_lat_text is None) != (end_lng_text is None):
        rejection_reasons.append("INCOMPLETE_END_COORDINATE_PAIR")

    end_lat = parse_coordinate(
        end_lat_text,
        "end_lat",
        -90,
        90,
        False,
        rejection_reasons,
    )
    end_lng = parse_coordinate(
        end_lng_text,
        "end_lng",
        -180,
        180,
        False,
        rejection_reasons,
    )

    has_missing_end_coordinates = end_lat is None and end_lng is None

    if has_missing_end_coordinates:
        quality_flags.append("MISSING_END_COORDINATES")

    is_long_trip = (
        duration_seconds is not None
        and duration_seconds > LONG_TRIP_THRESHOLD_SECONDS
    )

    if is_long_trip:
        quality_flags.append("LONG_TRIP_OVER_24_HOURS")

    rejection_reasons = list(dict.fromkeys(rejection_reasons))

    if rejection_reasons:
        return (
            None,
            tuple(rejection_reasons),
            tuple(quality_flags),
        )

    if ride_id is None:
        raise RuntimeError(
            "A row passed validation without a non-missing ride_id."
        )

    if rideable_type is None:
        raise RuntimeError(
            "A row passed validation without a rideable_type."
        )

    if member_casual is None:
        raise RuntimeError(
            "A row passed validation without a member type."
        )

    if started_at is None or ended_at is None:
        raise RuntimeError(
            "A row passed validation without valid timestamps."
        )

    if duration_seconds is None:
        raise RuntimeError(
            "A row passed validation without a calculated duration."
        )

    if start_station_name is None or start_station_id is None:
        raise RuntimeError(
            "A row passed validation without complete start-station data."
        )

    if start_lat is None or start_lng is None:
        raise RuntimeError(
            "A row passed validation without valid start coordinates."
        )

    seen_valid_ride_ids.add(ride_id)

    valid_database_row = (
        file_id,
        source_row_number,
        ride_id,
        rideable_type,
        started_at,
        ended_at,
        duration_seconds,
        start_station_name,
        start_station_id,
        end_station_name,
        reported_end_station_id,
        resolved_end_station_id,
        end_station_id_resolution_method,
        start_lat,
        start_lng,
        end_lat,
        end_lng,
        member_casual,
        is_long_trip,
        has_missing_end_station,
        has_missing_end_coordinates,
    )

    return (
        valid_database_row,
        (),
        tuple(quality_flags),
    )


def main() -> None:
    """Validate one raw Citi Bike file and load staging outcomes."""
    arguments = parse_arguments()
    file_id = arguments.file_id
    connection_parameters = get_connection_parameters()

    valid_rows: list[tuple[Any, ...]] = []
    rejected_rows: list[tuple[Any, ...]] = []
    quality_flag_counts: Counter[str] = Counter()
    rejection_reason_counts: Counter[str] = Counter()

    with psycopg.connect(**connection_parameters) as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            manifest_record = fetch_manifest_record(cursor, file_id)
            station_name_to_ids = build_station_name_to_ids(cursor)
            seen_valid_ride_ids = fetch_existing_valid_ride_ids(
                cursor,
                file_id,
            )
            raw_rows = fetch_raw_rows(cursor, file_id)

        expected_source_row_count = manifest_record["source_row_count"]

        if len(raw_rows) != expected_source_row_count:
            raise RuntimeError(
                "The manifest and raw table disagree before validation: "
                f"manifest={expected_source_row_count:,}, "
                f"raw={len(raw_rows):,}."
            )

        for raw_row in raw_rows:
            (
                valid_database_row,
                rejection_reasons,
                quality_flags,
            ) = validate_raw_row(
                raw_row,
                station_name_to_ids,
                seen_valid_ride_ids,
            )

            quality_flag_counts.update(quality_flags)

            if valid_database_row is not None:
                valid_rows.append(valid_database_row)
            else:
                rejection_reason_counts.update(rejection_reasons)
                rejected_rows.append(
                    (
                        raw_row["file_id"],
                        raw_row["source_row_number"],
                        normalize_text(raw_row["ride_id"]),
                        list(rejection_reasons),
                    )
                )

        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM staging.citibike_trip_valid
                WHERE file_id = %s;
                """,
                (file_id,),
            )
            cursor.execute(
                """
                DELETE FROM staging.citibike_trip_rejected
                WHERE file_id = %s;
                """,
                (file_id,),
            )

            if valid_rows:
                with cursor.copy(VALID_COPY_SQL) as copy:
                    for valid_row in valid_rows:
                        copy.write_row(valid_row)

            if rejected_rows:
                with cursor.copy(REJECTED_COPY_SQL) as copy:
                    for rejected_row in rejected_rows:
                        copy.write_row(rejected_row)

            cursor.execute(
                """
                SELECT
                    (
                        SELECT COUNT(*)
                        FROM source.citibike_trip_raw
                        WHERE file_id = %s
                    ) AS raw_row_count,
                    (
                        SELECT COUNT(*)
                        FROM staging.citibike_trip_valid
                        WHERE file_id = %s
                    ) AS valid_row_count,
                    (
                        SELECT COUNT(*)
                        FROM staging.citibike_trip_rejected
                        WHERE file_id = %s
                    ) AS rejected_row_count;
                """,
                (
                    file_id,
                    file_id,
                    file_id,
                ),
            )

            reconciliation_result = cursor.fetchone()

            if reconciliation_result is None:
                raise RuntimeError(
                    "The staging reconciliation query returned no result."
                )

            (
                database_raw_row_count,
                database_valid_row_count,
                database_rejected_row_count,
            ) = reconciliation_result

            if (
                database_raw_row_count
                != database_valid_row_count + database_rejected_row_count
            ):
                raise RuntimeError(
                    "Staging reconciliation failed: "
                    f"raw={database_raw_row_count:,}, "
                    f"valid={database_valid_row_count:,}, "
                    f"rejected={database_rejected_row_count:,}."
                )

    print("Citi Bike staging validation completed successfully.")
    print(f"File ID: {file_id}")
    print(f"Filename: {manifest_record['source_filename']}")
    print(f"Raw rows: {database_raw_row_count:,}")
    print(f"Valid rows: {database_valid_row_count:,}")
    print(f"Rejected rows: {database_rejected_row_count:,}")
    print(
        "Reconciliation: "
        f"{database_valid_row_count:,} + "
        f"{database_rejected_row_count:,} = "
        f"{database_raw_row_count:,}"
    )

    print("\nQuality flags among accepted rows:")

    if quality_flag_counts:
        for flag, count in quality_flag_counts.most_common():
            print(f"{flag}: {count:,}")
    else:
        print("None")

    print("\nRejection reasons:")

    if rejection_reason_counts:
        for reason, count in rejection_reason_counts.most_common():
            print(f"{reason}: {count:,}")
    else:
        print("None")


if __name__ == "__main__":
    main()
