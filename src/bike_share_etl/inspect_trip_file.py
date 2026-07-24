import csv
from collections import Counter
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

SAMPLE_SIZE = 5


def main() -> None:
    """Inspect the structure and completeness of the raw Citi Bike CSV file."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Data file not found: {DATA_FILE}")

    row_count = 0
    sample_rows: list[dict[str, str]] = []
    missing_counts: Counter[str] = Counter()

    with DATA_FILE.open(
        mode="r",
        encoding="utf-8-sig",
        newline="",
    ) as csv_file:
        reader = csv.DictReader(csv_file)

        if reader.fieldnames is None:
            raise ValueError("The CSV file does not contain a header row.")

        column_names = reader.fieldnames

        for row in reader:
            row_count += 1

            if len(sample_rows) < SAMPLE_SIZE:
                sample_rows.append(row.copy())

            for column_name in column_names:
                value = row.get(column_name)

                if value is None or value.strip() == "":
                    missing_counts[column_name] += 1

    display_path = DATA_FILE.relative_to(PROJECT_ROOT)

    print(f"File: {display_path}")
    print(f"Number of columns: {len(column_names)}")
    print(f"Number of data rows: {row_count:,}")

    print("\nColumns:")
    for position, column_name in enumerate(column_names, start=1):
        print(f"{position}. {column_name}")

    print("\nSample rows:")
    for row_number, row in enumerate(sample_rows, start=1):
        print(f"\nRow {row_number}:")

        for column_name in column_names:
            print(f"  {column_name}: {row[column_name]!r}")

    print("\nMissing-value counts:")
    for column_name in column_names:
        missing_count = missing_counts[column_name]

        if row_count == 0:
            missing_percentage = 0.0
        else:
            missing_percentage = 100 * missing_count / row_count

        print(
            f"{column_name}: "
            f"{missing_count:,} "
            f"({missing_percentage:.2f}%)"
        )


if __name__ == "__main__":
    main()
