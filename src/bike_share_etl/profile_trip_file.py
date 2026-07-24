import csv
import math
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import median


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "citibike"
    / "2025-01"
    / "JC-202501-citibike-tripdata.csv"
)

EXPECTED_COLUMNS = (
    "ride_id",
    "rideable_type",
    "started_at",
    "ended_at",
    "start_station_name",
    "start_station_id",
    "end_station_name",
    "end_station_id",
    "start_lat",
    "start_lng",
    "end_lat",
    "end_lng",
    "member_casual",
)

COORDINATE_COLUMNS = (
    "start_lat",
    "start_lng",
    "end_lat",
    "end_lng",
)


def is_missing(value: str | None) -> bool:
    """Return whether a CSV value is absent or contains only whitespace."""
    return value is None or value.strip() == ""


def parse_timestamp(value: str | None) -> datetime | None:
    """Parse an ISO-style timestamp, returning None when parsing fails."""
    if is_missing(value):
        return None

    try:
        return datetime.fromisoformat(value.strip())
    except ValueError:
        return None


def parse_finite_float(value: str | None) -> float | None:
    """Parse a finite floating-point value, returning None on failure."""
    if is_missing(value):
        return None

    try:
        parsed_value = float(value.strip())
    except ValueError:
        return None

    if not math.isfinite(parsed_value):
        return None

    return parsed_value


def update_minimum(
    current_minimum: float | None,
    candidate: float,
) -> float:
    """Return the smaller of the current minimum and a candidate value."""
    if current_minimum is None:
        return candidate

    return min(current_minimum, candidate)


def update_maximum(
    current_maximum: float | None,
    candidate: float,
) -> float:
    """Return the larger of the current maximum and a candidate value."""
    if current_maximum is None:
        return candidate

    return max(current_maximum, candidate)


def main() -> None:
    """Profile identifiers, categories, timestamps, stations, and coordinates."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Data file not found: {DATA_FILE}")

    row_count = 0

    ride_id_counts: Counter[str] = Counter()
    rideable_type_counts: Counter[str] = Counter()
    member_type_counts: Counter[str] = Counter()
    exact_row_counts: Counter[tuple[str, ...]] = Counter()

    missing_timestamp_counts: Counter[str] = Counter()
    invalid_timestamp_counts: Counter[str] = Counter()

    earliest_started_at: datetime | None = None
    latest_started_at: datetime | None = None
    earliest_ended_at: datetime | None = None
    latest_ended_at: datetime | None = None

    positive_durations_minutes: list[float] = []
    nonpositive_duration_count = 0
    over_24_hour_duration_count = 0

    end_station_missing_patterns: Counter[str] = Counter()
    end_coordinate_missing_patterns: Counter[str] = Counter()

    invalid_coordinate_counts: Counter[str] = Counter()
    out_of_range_coordinate_counts: Counter[str] = Counter()

    coordinate_minimums: dict[str, float | None] = {
        column_name: None for column_name in COORDINATE_COLUMNS
    }
    coordinate_maximums: dict[str, float | None] = {
        column_name: None for column_name in COORDINATE_COLUMNS
    }

    station_id_to_names: defaultdict[str, set[str]] = defaultdict(set)
    station_name_to_ids: defaultdict[str, set[str]] = defaultdict(set)

    with DATA_FILE.open(
        mode="r",
        encoding="utf-8-sig",
        newline="",
    ) as csv_file:
        reader = csv.DictReader(csv_file)

        if reader.fieldnames is None:
            raise ValueError("The CSV file does not contain a header row.")

        if tuple(reader.fieldnames) != EXPECTED_COLUMNS:
            raise ValueError(
                "The CSV schema differs from the expected schema.\n"
                f"Expected: {EXPECTED_COLUMNS}\n"
                f"Observed: {tuple(reader.fieldnames)}"
            )

        for row in reader:
            row_count += 1

            row_signature = tuple(
                row.get(column_name) or ""
                for column_name in EXPECTED_COLUMNS
            )
            exact_row_counts[row_signature] += 1

            ride_id = row["ride_id"].strip()
            if ride_id:
                ride_id_counts[ride_id] += 1

            rideable_type = row["rideable_type"].strip() or "<MISSING>"
            member_type = row["member_casual"].strip() or "<MISSING>"

            rideable_type_counts[rideable_type] += 1
            member_type_counts[member_type] += 1

            started_at_raw = row["started_at"]
            ended_at_raw = row["ended_at"]

            started_at = parse_timestamp(started_at_raw)
            ended_at = parse_timestamp(ended_at_raw)

            if is_missing(started_at_raw):
                missing_timestamp_counts["started_at"] += 1
            elif started_at is None:
                invalid_timestamp_counts["started_at"] += 1

            if is_missing(ended_at_raw):
                missing_timestamp_counts["ended_at"] += 1
            elif ended_at is None:
                invalid_timestamp_counts["ended_at"] += 1

            if started_at is not None:
                if earliest_started_at is None:
                    earliest_started_at = started_at
                    latest_started_at = started_at
                else:
                    earliest_started_at = min(
                        earliest_started_at,
                        started_at,
                    )
                    latest_started_at = max(
                        latest_started_at,
                        started_at,
                    )

            if ended_at is not None:
                if earliest_ended_at is None:
                    earliest_ended_at = ended_at
                    latest_ended_at = ended_at
                else:
                    earliest_ended_at = min(
                        earliest_ended_at,
                        ended_at,
                    )
                    latest_ended_at = max(
                        latest_ended_at,
                        ended_at,
                    )

            if started_at is not None and ended_at is not None:
                duration_minutes = (
                    ended_at - started_at
                ).total_seconds() / 60

                if duration_minutes <= 0:
                    nonpositive_duration_count += 1
                else:
                    positive_durations_minutes.append(duration_minutes)

                    if duration_minutes > 24 * 60:
                        over_24_hour_duration_count += 1

            end_station_name_missing = is_missing(
                row["end_station_name"]
            )
            end_station_id_missing = is_missing(
                row["end_station_id"]
            )

            if end_station_name_missing and end_station_id_missing:
                end_station_missing_patterns["both missing"] += 1
            elif end_station_name_missing:
                end_station_missing_patterns["name only missing"] += 1
            elif end_station_id_missing:
                end_station_missing_patterns["identifier only missing"] += 1
            else:
                end_station_missing_patterns["neither missing"] += 1

            end_lat_missing = is_missing(row["end_lat"])
            end_lng_missing = is_missing(row["end_lng"])

            if end_lat_missing and end_lng_missing:
                end_coordinate_missing_patterns["both missing"] += 1
            elif end_lat_missing:
                end_coordinate_missing_patterns["latitude only missing"] += 1
            elif end_lng_missing:
                end_coordinate_missing_patterns["longitude only missing"] += 1
            else:
                end_coordinate_missing_patterns["neither missing"] += 1

            for column_name in COORDINATE_COLUMNS:
                raw_coordinate = row[column_name]

                if is_missing(raw_coordinate):
                    continue

                coordinate = parse_finite_float(raw_coordinate)

                if coordinate is None:
                    invalid_coordinate_counts[column_name] += 1
                    continue

                coordinate_minimums[column_name] = update_minimum(
                    coordinate_minimums[column_name],
                    coordinate,
                )
                coordinate_maximums[column_name] = update_maximum(
                    coordinate_maximums[column_name],
                    coordinate,
                )

                if column_name.endswith("_lat"):
                    if not -90 <= coordinate <= 90:
                        out_of_range_coordinate_counts[column_name] += 1
                else:
                    if not -180 <= coordinate <= 180:
                        out_of_range_coordinate_counts[column_name] += 1

            for prefix in ("start", "end"):
                station_id = row[f"{prefix}_station_id"].strip()
                station_name = row[f"{prefix}_station_name"].strip()

                if station_id and station_name:
                    station_id_to_names[station_id].add(station_name)
                    station_name_to_ids[station_name].add(station_id)

    duplicated_ride_ids = {
        ride_id: count
        for ride_id, count in ride_id_counts.items()
        if count > 1
    }

    duplicated_ride_id_extra_rows = sum(
        count - 1 for count in duplicated_ride_ids.values()
    )

    exact_duplicate_extra_rows = sum(
        count - 1
        for count in exact_row_counts.values()
        if count > 1
    )

    station_ids_with_multiple_names = {
        station_id: sorted(names)
        for station_id, names in station_id_to_names.items()
        if len(names) > 1
    }

    station_names_with_multiple_ids = {
        station_name: sorted(station_ids)
        for station_name, station_ids in station_name_to_ids.items()
        if len(station_ids) > 1
    }

    display_path = DATA_FILE.relative_to(PROJECT_ROOT)

    print("SOURCE PROFILE")
    print("==============")
    print(f"File: {display_path}")
    print(f"Rows: {row_count:,}")
    print(f"Columns: {len(EXPECTED_COLUMNS)}")

    print("\nRIDE IDENTIFIERS")
    print("----------------")
    print(f"Unique non-missing ride IDs: {len(ride_id_counts):,}")
    print(f"Duplicated ride ID values: {len(duplicated_ride_ids):,}")
    print(
        "Additional rows caused by duplicated ride IDs: "
        f"{duplicated_ride_id_extra_rows:,}"
    )
    print(
        "Additional completely identical rows: "
        f"{exact_duplicate_extra_rows:,}"
    )

    print("\nRIDEABLE TYPES")
    print("--------------")
    for value, count in rideable_type_counts.most_common():
        print(f"{value}: {count:,}")

    print("\nMEMBERSHIP TYPES")
    print("----------------")
    for value, count in member_type_counts.most_common():
        print(f"{value}: {count:,}")

    print("\nTIMESTAMPS")
    print("----------")
    print(f"Earliest start: {earliest_started_at}")
    print(f"Latest start: {latest_started_at}")
    print(f"Earliest end: {earliest_ended_at}")
    print(f"Latest end: {latest_ended_at}")
    print(
        "Missing started_at values: "
        f"{missing_timestamp_counts['started_at']:,}"
    )
    print(
        "Invalid started_at values: "
        f"{invalid_timestamp_counts['started_at']:,}"
    )
    print(
        "Missing ended_at values: "
        f"{missing_timestamp_counts['ended_at']:,}"
    )
    print(
        "Invalid ended_at values: "
        f"{invalid_timestamp_counts['ended_at']:,}"
    )

    print("\nTRIP DURATIONS")
    print("--------------")
    print(f"Nonpositive durations: {nonpositive_duration_count:,}")
    print(
        "Positive durations over 24 hours: "
        f"{over_24_hour_duration_count:,}"
    )

    if positive_durations_minutes:
        print(
            "Minimum positive duration in minutes: "
            f"{min(positive_durations_minutes):.3f}"
        )
        print(
            "Median positive duration in minutes: "
            f"{median(positive_durations_minutes):.3f}"
        )
        print(
            "Maximum positive duration in minutes: "
            f"{max(positive_durations_minutes):.3f}"
        )

    print("\nEND-STATION MISSINGNESS")
    print("-----------------------")
    for pattern, count in end_station_missing_patterns.items():
        print(f"{pattern}: {count:,}")

    print("\nEND-COORDINATE MISSINGNESS")
    print("--------------------------")
    for pattern, count in end_coordinate_missing_patterns.items():
        print(f"{pattern}: {count:,}")

    print("\nCOORDINATES")
    print("-----------")
    for column_name in COORDINATE_COLUMNS:
        print(
            f"{column_name}: "
            f"minimum={coordinate_minimums[column_name]}, "
            f"maximum={coordinate_maximums[column_name]}, "
            f"invalid={invalid_coordinate_counts[column_name]:,}, "
            "out_of_range="
            f"{out_of_range_coordinate_counts[column_name]:,}"
        )

    print("\nSTATION CONSISTENCY")
    print("-------------------")
    print(
        "Station IDs associated with multiple names: "
        f"{len(station_ids_with_multiple_names):,}"
    )
    print(
        "Station names associated with multiple IDs: "
        f"{len(station_names_with_multiple_ids):,}"
    )

    if station_ids_with_multiple_names:
        print("\nExamples of station IDs with multiple names:")
        for station_id, names in list(
            station_ids_with_multiple_names.items()
        )[:10]:
            print(f"{station_id}: {names}")

    if station_names_with_multiple_ids:
        print("\nExamples of station names with multiple IDs:")
        for station_name, station_ids in list(
            station_names_with_multiple_ids.items()
        )[:10]:
            print(f"{station_name}: {station_ids}")


if __name__ == "__main__":
    main()