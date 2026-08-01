# Docker Compose PostgreSQL Environment

## Purpose

This milestone introduces a reproducible PostgreSQL environment without replacing the earlier direct Windows installation. The same ingestion, validation, and dbt workflows can now be executed against a clean PostgreSQL instance created by Docker Compose.

## Service definition

`compose.yml` defines one service:

```text
postgres
```

The service uses the official image:

```text
postgres:18.4
```

The project does not build a custom PostgreSQL image. Docker pulls the existing image and creates a container from it.

## Environment variables

The service reads:

- `DB_NAME`;
- `DB_USER`;
- `DB_PASSWORD`;
- `DOCKER_DB_PORT`.

Private values remain in the ignored `.env` file. `.env.example` documents the required configuration without including credentials.

## Port isolation

The direct Windows PostgreSQL installation remains available at:

```text
localhost:5432
```

The containerized PostgreSQL service is exposed at:

```text
localhost:5433
```

The Compose mapping is:

```text
host 5433 -> container 5432
```

This makes the two database instances independent and prevents a port collision.

## Persistent storage

The named volume:

```text
citibike_postgres_data
```

is mounted at:

```text
/var/lib/postgresql
```

The volume stores PostgreSQL data outside the disposable container layer.

```bash
docker compose down
```

removes the container and network while preserving the volume.

```bash
docker compose down --volumes
```

also removes the database volume and its contents.

## Initialization scripts

The existing SQL definitions are mounted read-only into:

```text
/docker-entrypoint-initdb.d/
```

Execution order:

1. `001_create_citibike_raw_tables.sql`
2. `002_create_citibike_staging_tables.sql`
3. `003_create_pipeline_run_table.sql`

On the first startup of an empty PostgreSQL volume, these files create the `source`, `staging`, and `operations` schemas and their foundational tables.

The scripts do not create the dbt view or mart table. dbt creates the `analytics` schema and its relations during `dbt build`.

The official PostgreSQL initialization mechanism runs these scripts only when the data directory is empty. Adding a new file to `/docker-entrypoint-initdb.d/` does not execute it against an already initialized volume.

## Health check

The service health check uses `pg_isready` with the configured database and user. A healthy state indicates that PostgreSQL is accepting connections, not merely that the container process exists.

## Verified workflow

The following workflow was executed successfully against the Docker database:

```text
Fresh PostgreSQL container
        |
        v
Initialization SQL creates empty tables
        |
        v
Python loads the source CSV
        |
        v
Python validates raw rows into staging
        |
        v
dbt creates the analytical view and table
        |
        v
all dbt tests pass
```

Verified row counts:

| Relation | Rows |
|---|---:|
| `source.citibike_trip_raw` | 50,611 |
| `staging.citibike_trip_valid` | 50,611 |
| `staging.citibike_trip_rejected` | 0 |
| `analytics.stg_citibike_trips` | 50,611 |
| `analytics.daily_citibike_activity` | 126 |

Verified relation types:

| Relation | Type |
|---|---|
| `analytics.stg_citibike_trips` | `VIEW` |
| `analytics.daily_citibike_activity` | `BASE TABLE` |

Verified dbt result:

```text
PASS=36 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=36
```

This total contains 34 data tests and two model-building operations.

## Current boundary

PostgreSQL is containerized, but Python and dbt still execute from the Windows host virtual environment. The next milestone will add an application image and Compose service so that Python, Psycopg, pytest, Ruff, and dbt can execute inside Docker as well.
