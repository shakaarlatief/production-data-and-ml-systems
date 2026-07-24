import csv
import hashlib
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"

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

HASH_CHUNK_SIZE_BYTES = 1024 * 1024

COPY_SQL = """
    COPY source.citibike_trip_raw (
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
    )
    FROM STDIN
"""


def calculate_sha256(file_path: Path) -> str:
    """Calculate the SHA-256 hash of a file without loading it all into memory."""
    digest = hashlib.sha256()

    with file_path.open(mode="rb") as source_file:
        while True:
            chunk = source_file.read(HASH_CHUNK_SIZE_BYTES)

            if chunk == b"":
                break

            digest.update(chunk)

    return digest.hexdigest()


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


def main() -> None:
    """Register and load one Citi Bike source file transactionally."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Data file not found: {DATA_FILE}")

    source_sha256 = calculate_sha256(DATA_FILE)
    source_file_size_bytes = DATA_FILE.stat().st_size
    connection_parameters = get_connection_parameters()

    loaded_row_count = 0
    file_id: int | None = None

    with psycopg.connect(**connection_parameters) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO source.citibike_file (
                    source_filename,
                    source_sha256,
                    source_file_size_bytes,
                    source_row_count
                )
                VALUES (%s, %s, %s, 0)
                ON CONFLICT (source_sha256)
                DO NOTHING
                RETURNING file_id;
                """,
                (
                    DATA_FILE.name,
                    source_sha256,
                    source_file_size_bytes,
                ),
            )

            inserted_file = cursor.fetchone()

            if inserted_file is None:
                cursor.execute(
                    """
                    SELECT
                        file_id,
                        source_filename,
                        source_row_count,
                        loaded_at
                    FROM source.citibike_file
                    WHERE source_sha256 = %s;
                    """,
                    (source_sha256,),
                )

                existing_file = cursor.fetchone()

                if existing_file is None:
                    raise RuntimeError(
                        "The file was not inserted, but no existing "
                        "manifest record could be found."
                    )

                (
                    existing_file_id,
                    existing_filename,
                    existing_row_count,
                    existing_loaded_at,
                ) = existing_file

                print("File already loaded. No rows were inserted.")
                print(f"Existing file ID: {existing_file_id}")
                print(f"Existing filename: {existing_filename}")
                print(f"Existing row count: {existing_row_count:,}")
                print(f"Originally loaded at: {existing_loaded_at}")
                return

            file_id = inserted_file[0]

            with DATA_FILE.open(
                mode="r",
                encoding="utf-8-sig",
                newline="",
            ) as csv_file:
                reader = csv.DictReader(csv_file)

                if reader.fieldnames is None:
                    raise ValueError(
                        "The CSV file does not contain a header row."
                    )

                if tuple(reader.fieldnames) != EXPECTED_COLUMNS:
                    raise ValueError(
                        "The CSV schema differs from the expected schema.\n"
                        f"Expected: {EXPECTED_COLUMNS}\n"
                        f"Observed: {tuple(reader.fieldnames)}"
                    )

                with cursor.copy(COPY_SQL) as copy:
                    for source_row_number, row in enumerate(
                        reader,
                        start=1,
                    ):
                        if None in row:
                            raise ValueError(
                                "A CSV row contains more values than the "
                                f"header defines. Source row: "
                                f"{source_row_number}"
                            )

                        database_row: list[int | str | None] = [
                            file_id,
                            source_row_number,
                        ]

                        for column_name in EXPECTED_COLUMNS:
                            database_row.append(row[column_name])

                        copy.write_row(database_row)
                        loaded_row_count += 1

            cursor.execute(
                """
                UPDATE source.citibike_file
                SET source_row_count = %s
                WHERE file_id = %s;
                """,
                (
                    loaded_row_count,
                    file_id,
                ),
            )

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM source.citibike_trip_raw
                WHERE file_id = %s;
                """,
                (file_id,),
            )

            count_result = cursor.fetchone()

            if count_result is None:
                raise RuntimeError(
                    "The raw-row reconciliation query returned no result."
                )

            database_row_count = count_result[0]

            if database_row_count != loaded_row_count:
                raise RuntimeError(
                    "Raw-row reconciliation failed: "
                    f"Python loaded {loaded_row_count:,} rows, "
                    f"but PostgreSQL contains {database_row_count:,} rows."
                )

    print("Raw file load completed successfully.")
    print(f"File ID: {file_id}")
    print(f"Filename: {DATA_FILE.name}")
    print(f"SHA-256: {source_sha256}")
    print(f"File size in bytes: {source_file_size_bytes:,}")
    print(f"Rows loaded: {loaded_row_count:,}")


if __name__ == "__main__":
    main()