# Current Status and Next Actions

## Repository purpose

This repository is a separate learning and portfolio programme for production data and machine-learning systems. It is not part of the Telco Customer Churn classification repository.

The current implementation uses a compact Citi Bike batch pipeline to make database, transformation, testing, and infrastructure concepts concrete before larger orchestration, cloud, distributed-processing, and MLOps components are introduced.

## Active phase

**Phase 4: Analytics engineering and reproducible data environments**

The direct Python, Psycopg, PostgreSQL, explicit-SQL, dbt Core, and PostgreSQL Docker Compose foundations are complete enough to support the next infrastructure milestone.

## Active lesson

**Containerizing the Python and dbt execution environment**

PostgreSQL now runs reproducibly in Docker Compose, while Python and dbt still execute from the Windows host and the local `.venv`. The next objective is to build an application image that contains the project runtime and can execute ingestion, validation, tests, and dbt commands without depending on host-installed Python packages.

## Completed implementation

The Citi Bike case study now includes:

- immutable local raw-file handling;
- a reproducible raw landing layer;
- a typed accepted-record and rejected-record staging layer;
- deterministic rerun behavior;
- source-to-database and raw-to-staging reconciliation;
- controlled synthetic validation fixtures;
- automated Python unit tests and Ruff checks;
- reproducible Python dependency configuration;
- a persistent PostgreSQL table for pipeline-run audit records;
- a dbt Core project connected to PostgreSQL;
- declared dbt sources for validated and rejected staging data;
- a ride-level dbt staging view;
- a physically stored daily analytical mart;
- generic and singular dbt data tests;
- generated dbt documentation and verified lineage;
- a Docker Compose PostgreSQL service;
- environment-variable configuration through `.env` and `.env.example`;
- a persistent PostgreSQL named volume;
- read-only bind mounts for database initialization SQL;
- a PostgreSQL health check;
- an isolated host-to-container port mapping;
- verified Python and dbt execution against the containerized database.

## Practical environment

- PostgreSQL 18 remains installed locally on Windows at `localhost:5432`.
- Docker Compose runs a separate PostgreSQL 18.4 service at `localhost:5433`.
- pgAdmin 4 can inspect either database when configured with the corresponding port.
- A Python 3.11 virtual environment remains available on the host.
- Local credentials are loaded from an ignored `.env` file.
- The repository is installable in editable mode through `pyproject.toml`.
- Pytest, Ruff, dbt Core, and the PostgreSQL dbt adapter are installed through the optional `dev` dependency group.
- Docker Desktop, Docker Compose, and VS Code Container Tools are available for container management and inspection.

## Source evidence

The first source file is:

`JC-202501-citibike-tripdata.csv`

Observed grain:

`one row per recorded bicycle ride`

Observed structure:

- 50,611 data rows;
- 13 source columns;
- unique ride identifiers in the observed file;
- no exact duplicate source rows;
- two observed bicycle categories;
- two observed membership categories;
- parseable start and end timestamps;
- valid non-missing geographic coordinates.

Important quality findings:

| Finding | Count |
|---|---:|
| Trips longer than 24 hours | 21 |
| Missing end-station identifiers inferred uniquely from names | 25 |
| Rows without a resolved end station | 107 |
| Rows without end coordinates | 19 |

Station identifier `JC075` appears with two source-name variants. Station identifiers are therefore treated as the stable station reference, while source names are preserved as descriptive values.

## Raw landing layer completed

Implemented tables:

- `source.citibike_file`
- `source.citibike_trip_raw`

Implemented behavior:

- SHA-256 file identity;
- source-file manifest metadata;
- immutable raw values stored as text;
- row lineage through `(file_id, source_row_number)`;
- PostgreSQL `COPY` loading;
- transactional ingestion;
- raw-row reconciliation;
- idempotent repeated execution of the same file.

Verified result:

| Measure | Count |
|---|---:|
| Manifest source rows | 50,611 |
| Raw database rows | 50,611 |
| Duplicate rows inserted on second execution | 0 |

## Validated staging layer completed

Implemented tables:

- `staging.citibike_trip_valid`
- `staging.citibike_trip_rejected`

The validation process:

- converts blank text to explicit missing values;
- parses timestamps and coordinates;
- calculates trip duration;
- validates required values and accepted categories;
- rejects technically invalid records with explicit reason codes;
- retains usable unusual records through soft quality flags;
- preserves provider-reported station identifiers;
- derives a separate resolved station identifier when inference is deterministic;
- replaces one file's staging outcomes transactionally on rerun;
- verifies `raw rows = valid rows + rejected rows`.

Verified result:

| Measure | Count |
|---|---:|
| Raw rows | 50,611 |
| Valid rows | 50,611 |
| Rejected rows | 0 |
| Reconciliation | 50,611 = 50,611 + 0 |

## Automated Python validation completed

A controlled synthetic fixture is stored separately under `tests/fixtures/`. It does not modify or imitate the real raw dataset.

The fixture exercises:

- a normal valid trip;
- a long trip with missing endpoint information;
- deterministic and ambiguous station-name resolution;
- missing ride identifier;
- invalid timestamp text;
- nonpositive duration;
- unknown categorical values;
- invalid and incomplete coordinates;
- duplicate ride identifiers.

Verified result:

```text
12 passed
All checks passed!
```

## Pipeline-run audit structure completed

Implemented table:

- `operations.pipeline_run`

Grain:

`one row per execution of one pipeline stage`

The table supports:

- pipeline and stage names;
- a reference to the processed source file when available;
- `running`, `succeeded`, and `failed` statuses;
- timezone-aware start and finish timestamps;
- source, valid, and rejected row counts;
- error type and message fields;
- supplementary `JSONB` details;
- constraints that prevent contradictory run states;
- indexes for pipeline-time and source-file lookups.

The structure exists in both the direct Windows PostgreSQL database and the reproducibly initialized containerized database. The Python ingestion and validation programs do not yet write audit records automatically.

## dbt Core analytics layer completed

The repository contains a dbt Core project configured through `dbt_project.yml` and `dbt/profiles.yml`. Database credentials are read from environment variables, so secrets remain outside version control.

Declared sources:

- `staging.citibike_trip_valid`
- `staging.citibike_trip_rejected`

Implemented models:

### `analytics.stg_citibike_trips`

Materialization:

`view`

Grain:

`one row per accepted bicycle ride`

The model preserves the validated ride-level data while adding:

- `ride_date`;
- `start_hour`;
- `duration_minutes`.

### `analytics.daily_citibike_activity`

Materialization:

`table`

Grain:

`one row per ride date, bicycle type, and membership category`

The model stores:

- trip count;
- average duration in minutes;
- long-trip count;
- missing-end-station count;
- missing-end-coordinate count.

Implemented verification includes:

- source `not_null` and `unique` tests;
- model `not_null`, `unique`, and `accepted_values` tests;
- a singular grain test;
- a singular measure-bound test;
- a singular ride-level-to-summary reconciliation test.

Full containerized-database build result:

```text
Found 2 models, 34 data tests, 2 sources
PASS=36 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=36
```

The total consists of 34 data tests, one view model, and one table model.

Generated dbt documentation and lineage were previously verified. The dependency chain remains:

```text
citibike.trip_valid
        -> stg_citibike_trips
        -> daily_citibike_activity
        -> project-specific singular tests
```

## Docker Compose PostgreSQL milestone completed

The repository now contains:

- `compose.yml`;
- `.env.example`.

The Compose project defines one PostgreSQL service using:

```text
postgres:18.4
```

The service configuration includes:

- database name, user, and password supplied through environment variables;
- host port `${DOCKER_DB_PORT:-5433}` mapped to container port `5432`;
- a named volume called `citibike_postgres_data`;
- a health check based on `pg_isready`;
- read-only bind mounts for the three existing SQL initialization files.

The bind-mounted initialization files are exposed inside the container under `/docker-entrypoint-initdb.d/`:

1. `001_create_citibike_raw_tables.sql`
2. `002_create_citibike_staging_tables.sql`
3. `003_create_pipeline_run_table.sql`

On first initialization of an empty PostgreSQL volume, these scripts create:

- `source.citibike_file`;
- `source.citibike_trip_raw`;
- `staging.citibike_trip_valid`;
- `staging.citibike_trip_rejected`;
- `operations.pipeline_run`.

The `analytics` schema is not created by the three SQL scripts. dbt creates it when the analytical models are built.

Verified container status:

```text
production-data-and-ml-systems-postgres-1
postgres:18.4
healthy
0.0.0.0:5433->5432/tcp
```

Verified foundational schemas after recreating the initially empty volume:

- `source`;
- `staging`;
- `operations`;
- `public`.

Verified foundational tables:

| Schema | Table |
|---|---|
| `source` | `citibike_file` |
| `source` | `citibike_trip_raw` |
| `staging` | `citibike_trip_valid` |
| `staging` | `citibike_trip_rejected` |
| `operations` | `pipeline_run` |

## End-to-end containerized database evidence

The existing host Python and dbt runtimes were pointed at the Docker PostgreSQL service through port `5433`.

Verified row counts:

| Layer | Object | Rows |
|---|---|---:|
| Raw | `source.citibike_trip_raw` | 50,611 |
| Validated | `staging.citibike_trip_valid` | 50,611 |
| Rejected | `staging.citibike_trip_rejected` | 0 |
| dbt staging | `analytics.stg_citibike_trips` | 50,611 |
| dbt mart | `analytics.daily_citibike_activity` | 126 |

Verified analytical relation types:

| Object | PostgreSQL relation type |
|---|---|
| `analytics.stg_citibike_trips` | `VIEW` |
| `analytics.daily_citibike_activity` | `BASE TABLE` |

This evidence demonstrates that the database software, foundational schema, raw ingestion, staging validation, dbt transformation, and dbt testing workflow can be reproduced against a fresh containerized PostgreSQL instance.

## Reproducible Python project configuration

`pyproject.toml` records:

- the supported Python version;
- runtime dependencies;
- optional development dependencies;
- package discovery under `src/`;
- pytest configuration;
- Ruff configuration;
- dbt Core and the PostgreSQL adapter through the development dependency group.

The package is installed locally with:

```bash
python -m pip install -e ".[dev]"
```

Generated `*.egg-info/` package metadata, dbt `target/`, dbt logs, and downloaded dbt packages are excluded from version control.

## Evidence boundary

Evidence now supports claims that the case study includes:

- real-file profiling;
- reproducible raw, staging, operations, and analytics definitions;
- transactional raw ingestion;
- SHA-256-based idempotency;
- typed validation;
- explicit accepted and rejected outcomes;
- hard rules and soft quality flags;
- deterministic enrichment with source-value preservation;
- raw-to-staging reconciliation;
- rerun-safe staging replacement;
- controlled synthetic test fixtures;
- automated Python unit tests;
- repeatable lint and test commands;
- a verified pipeline-run audit table structure;
- a dbt Core project connected to PostgreSQL;
- dbt-managed view and table models;
- dependency-aware builds through `source()` and `ref()`;
- generic and singular dbt data tests;
- generated dbt documentation and lineage;
- a containerized PostgreSQL service;
- persistent database storage through a named volume;
- automatic foundational-schema initialization on an empty volume;
- database health checks;
- isolated local port mapping;
- successful host-based Python and dbt execution against the containerized database;
- complete row-count and relation-type verification in the containerized database.

Evidence does not yet support claims that the repository includes:

- a containerized Python application runtime;
- a containerized dbt runtime;
- automatic pipeline-run audit writes;
- structured production logging;
- centralized shared configuration and database utilities;
- workflow orchestration;
- continuous integration;
- cloud deployment;
- distributed processing;
- production monitoring.

## Immediate next actions

1. Add a project `Dockerfile` for a reproducible Python 3.11 application image.
2. Add a `.dockerignore` file so local virtual environments, generated artifacts, secrets, and raw data are not copied into the image unintentionally.
3. Install the repository and its development dependencies inside the image.
4. Add an application service to `compose.yml` that communicates with PostgreSQL through the Compose network using the service hostname `postgres`, rather than `localhost`.
5. Make the application service wait for the PostgreSQL health check before running database-dependent commands.
6. Execute Python connection checks, tests, ingestion, validation, and dbt commands from the application container.
7. Verify that a clean machine requires Docker and the raw input file, but does not require host-installed PostgreSQL, Python packages, Psycopg, or dbt.
8. Update documentation and merge the application-runtime milestone before introducing orchestration or continuous integration.

## Current implementation boundary

The completed implementation covers environment setup, secure local configuration, database connectivity, real-source acquisition, detailed profiling, raw landing, typed validation, accepted and rejected outcomes, transactional bulk loading, deterministic reruns, row-count reconciliation, synthetic test fixtures, automated tests, lint configuration, a persistent pipeline-run audit table, a tested and documented dbt analytics layer, and a fully verified Docker Compose PostgreSQL environment.

PostgreSQL is containerized. Python and dbt are not yet containerized. No scheduled workflow, cloud resource, distributed pipeline, or machine-learning system has been completed.

## Deferred until prerequisites are ready

- advanced PostgreSQL administration;
- recursive CTEs;
- triggers and stored procedures;
- deep transaction-isolation and locking analysis;
- partitioning and advanced index types;
- Airflow or another orchestrator;
- MLflow;
- Azure;
- NoSQL implementations;
- Spark;
- Kafka;
- Kubernetes;
- Terraform.

## Update rule

This document is the tactical source of truth. It should be updated whenever the active lesson, immediate next action, implementation boundary, or repository inclusion decision changes.
