import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"


def main() -> None:
    """Open a PostgreSQL connection and verify which database is active."""
    if not ENV_FILE.exists():
        raise FileNotFoundError(
            f"Environment configuration file not found: {ENV_FILE}"
        )

    load_dotenv(dotenv_path=ENV_FILE)

    connection_parameters = {
        "host": os.environ["DB_HOST"],
        "port": os.environ["DB_PORT"],
        "dbname": os.environ["DB_NAME"],
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
    }

    with psycopg.connect(**connection_parameters) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    current_database(),
                    current_user,
                    version();
                """
            )

            result = cursor.fetchone()

            if result is None:
                raise RuntimeError(
                    "The database verification query returned no result."
                )

            database_name, database_user, database_version = result

    print(f"Connected database: {database_name}")
    print(f"Connected user: {database_user}")
    print(f"PostgreSQL version: {database_version}")


if __name__ == "__main__":
    main()
