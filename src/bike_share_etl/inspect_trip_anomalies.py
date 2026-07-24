import csv
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "citibike"
    / "2025-01"
    / "JC-202501-citibike-tripdata.csv"
)

PERIOD_START = datetime(2025, 1, 1)
PERIOD_END = datetime(2025, 2, 1)

EXAMPLE_LIMIT = 10


def is_missing(value: str | None) -> bool:
    """Return whether a CSV value is absent or contains only whitespace."""
    return value is None or value.strip() == ""


def parse_timestamp(value: str) -> datetime:
    """Parse a timestamp that has already passed source profiling."""
    return datetime.fromisoformat(value.strip())


def main() -> None:
    """Inspect unresolved source anomalies before table design."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Data file not found: {DATA_FILE}")

    station_name_to_ids: defaultdict[str, set[str]] = defaultdict(set)
    station_name_counts: Counter[tuple[str, str]] = Counter()

    rows_with_missing_end_id: list[dict[str, str]] = []
    rows_with_missing_end_station: list[dict[str, str]] = []
    rows_with_missing_end_coordinates: list[dict[str, str]] = []
    rows_outside_file_period: list[dict[str, str]] = []
    long_trip_rows: list[tuple[float, dict[str, str]]] = []

    missingness_relationships: Counter[tuple[str, str]] = Counter()

    with DATA_FILE.open(
        mode="r",
        encoding="utf-8-sig",
        newline="",
    ) as csv_file:
        reader = csv.DictReader(csv_file)

        if reader.fieldnames is None:
            raise ValueError("The CSV file does not contain a header row.")

        for row in reader:
            for prefix in ("start", "end"):
                station_name = row[f"{prefix}_station_name"].strip()
                station_id = row[f"{prefix}_station_id"].strip()

                if station_name and station_id:
                    station_name_to_ids[station_name].add(station_id)
                    station_name_counts[(station_id, station_name)] += 1

            started_at = parse_timestamp(row["started_at"])
            ended_at = parse_timestamp(row["ended_at"])

            duration_minutes = (
                ended_at - started_at
            ).total_seconds() / 60

            if duration_minutes > 24 * 60:
                long_trip_rows.append((duration_minutes, row.copy()))

            if not PERIOD_START <= started_at < PERIOD_END:
                rows_outside_file_period.append(row.copy())

            end_name_missing = is_missing(row["end_station_name"])
            end_id_missing = is_missing(row["end_station_id"])
            end_lat_missing = is_missing(row["end_lat"])
            end_lng_missing = is_missing(row["end_lng"])

            if end_name_missing and end_id_missing:
                station_status = "both station fields missing"
                rows_with_missing_end_station.append(row.copy())
            elif end_id_missing:
                station_status = "station ID missing"
                rows_with_missing_end_id.append(row.copy())
            elif end_name_missing:
                station_status = "station name missing"
            else:
                station_status = "station fields complete"

            if end_lat_missing and end_lng_missing:
                coordinate_status = "both coordinates missing"
                rows_with_missing_end_coordinates.append(row.copy())
            elif end_lat_missing or end_lng_missing:
                coordinate_status = "one coordinate missing"
            else:
                coordinate_status = "coordinates complete"

            missingness_relationships[
                (station_status, coordinate_status)
            ] += 1

    long_trip_rows.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    inferred_end_ids: Counter[str] = Counter()
    inference_examples: list[
        tuple[str, set[str], str]
    ] = []

    for row in rows_with_missing_end_id:
        station_name = row["end_station_name"].strip()
        possible_ids = station_name_to_ids.get(station_name, set())

        if len(possible_ids) == 1:
            inference_status = "unique match"
        elif len(possible_ids) > 1:
            inference_status = "multiple matches"
        else:
            inference_status = "no match"

        inferred_end_ids[inference_status] += 1

        if len(inference_examples) < EXAMPLE_LIMIT:
            inference_examples.append(
                (
                    station_name,
                    possible_ids,
                    row["ride_id"],
                )
            )

    display_path = DATA_FILE.relative_to(PROJECT_ROOT)

    print("TARGETED ANOMALY INSPECTION")
    print("===========================")
    print(f"File: {display_path}")

    print("\nFILE-PERIOD BOUNDARIES")
    print("----------------------")
    print(
        "Rows whose started_at falls outside January 2025: "
        f"{len(rows_outside_file_period):,}"
    )

    for row in rows_outside_file_period[:EXAMPLE_LIMIT]:
        print(
            f"{row['ride_id']}: "
            f"{row['started_at']} -> {row['ended_at']}"
        )

    print("\nTRIPS LONGER THAN 24 HOURS")
    print("--------------------------")
    print(f"Count: {len(long_trip_rows):,}")

    for duration_minutes, row in long_trip_rows[:EXAMPLE_LIMIT]:
        print(
            f"{row['ride_id']}: "
            f"{duration_minutes:.3f} minutes, "
            f"{row['started_at']} -> {row['ended_at']}, "
            f"{row['start_station_name']!r} -> "
            f"{row['end_station_name']!r}"
        )

    print("\nMISSING END-STATION IDENTIFIERS")
    print("-------------------------------")
    print(
        "Rows with an end-station name but no identifier: "
        f"{len(rows_with_missing_end_id):,}"
    )

    for status, count in inferred_end_ids.items():
        print(f"{status}: {count:,}")

    print("\nInference examples:")
    for station_name, possible_ids, ride_id in inference_examples:
        print(
            f"{ride_id}: "
            f"name={station_name!r}, "
            f"observed IDs={sorted(possible_ids)}"
        )

    print("\nMISSINGNESS RELATIONSHIPS")
    print("-------------------------")
    for relationship, count in missingness_relationships.most_common():
        station_status, coordinate_status = relationship
        print(
            f"{station_status}; "
            f"{coordinate_status}: "
            f"{count:,}"
        )

    print("\nJC075 NAME VARIANTS")
    print("-------------------")
    for (station_id, station_name), count in station_name_counts.items():
        if station_id == "JC075":
            print(f"{station_name!r}: {count:,}")


if __name__ == "__main__":
    main()