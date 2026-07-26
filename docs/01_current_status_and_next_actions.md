# Current Status and Next Actions

## Repository purpose

This repository is a separate learning and portfolio programme for production data and machine-learning systems. It is not part of the Telco Customer Churn classification repository.

## Active phase

**Phase 4: Analytics engineering and reproducible data environments**

The direct Python, Psycopg, PostgreSQL, and explicit-SQL foundation is complete enough to support higher-level tools. The first dedicated analytics-engineering milestone has now been completed with dbt Core. The next phase introduces containerization so that the database and transformation environment can be reproduced without depending on a manually configured local machine.

## Active lesson

**Docker and Docker Compose fundamentals**

The Citi Bike case study now has:

- a reproducible raw landing layer;
- a typed accepted-record and rejected-record staging layer;
- deterministic rerun behavior;
- source-to-database reconciliation;
- controlled synthetic validation fixtures;
- automated Python unit tests and Ruff checks;
- reproducible Python dependency configuration;
- a persistent PostgreSQL table for pipeline-run audit records;
- a dbt Core project connected to PostgreSQL;
- declared dbt sources for validated and rejected staging data;
- a ride-level staging view;
- a physically stored daily analytical mart;
- generic and singular dbt data tests;
- generated dbt documentation and verified lineage.

The immediate objective is to introduce Docker and Docker Compose without expanding the bicycle-domain analysis unnecessarily. The goal is to understand images, containers, services, networks, volumes, environment variables, health checks, and reproducible multi-service startup before orchestration or cloud abstractions are added.

## Practical environment

- PostgreSQL 18 is installed locally and running.
- pgAdmin 4 is connected to the local PostgreSQL server.
- A Python 3.11 virtual environment is used for this repository.
- Local credentials are loaded from an ignored `.env` file.
- A dedicated `bike_share_etl` database is available.
- The `source`, `staging`, `analytics`, and `operations` schemas exist inside `bike_share_etl`.
- The official January 2025 Jersey City Citi Bike file is stored locally under ignored raw-data storage.
- The repository is installable in editable mode through `pyproject.toml`.
- Pytest, Ruff, dbt Core, and the PostgreSQL dbt adapter are installed through the optional `dev` dependency group.

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

Observed result:

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

Observed result from two identical validation executions:

| Measure | Count |
|---|---:|
| Raw rows | 50,611 |
| Valid rows | 50,611 |
| Rejected rows | 0 |
| Reconciliation | 50,611 + 0 = 50,611 |

## Automated Python validation evidence completed

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

Automated verification result:

```text
12 passed
All checks passed!
```

The tests verify that hard failures produce explicit rejection reasons and that soft conditions remain accepted while producing explicit quality flags.

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

The table has been created and verified in the local PostgreSQL database. Its initial row count is zero. The current Python ingestion and validation programs do not yet write audit records automatically, so the structure exists but operational integration remains future work.

## dbt Core analytics layer completed

The repository now contains a dbt Core project configured through `dbt_project.yml` and `dbt/profiles.yml`. Database credentials are read from environment variables, so secrets remain outside version control.

Declared sources:

- `staging.citibike_trip_valid`
- `staging.citibike_trip_rejected`

Implemented dbt models:

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

Implemented dbt verification includes:

- source `not_null` and `unique` tests;
- model `not_null`, `unique`, and `accepted_values` tests;
- a singular grain test;
- a singular measure-bound test;
- a singular ride-level-to-summary reconciliation test.

Verified selected dependency-chain build:

```text
Found 2 models, 34 data tests, 2 sources
PASS=33 WARN=0 ERROR=0 SKIP=0 TOTAL=33
```

The selected build excluded the three tests attached only to `citibike.trip_rejected`, because that source is not an ancestor of `daily_citibike_activity`.

Generated dbt documentation was opened locally and the lineage graph was verified:

```text
citibike.trip_valid
        -> stg_citibike_trips
        -> daily_citibike_activity
        -> project-specific singular tests
```

The rejected-record source appears as a separate documented source because no current analytical model depends on it.

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

Evidence supports claims that the case study includes:

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
- generated dbt documentation and lineage.

Evidence does not yet support claims that the repository includes:

- automatic pipeline-run audit writes;
- structured production logging;
- centralized shared configuration and database utilities;
- containerization;
- workflow orchestration;
- continuous integration;
- cloud deployment;
- distributed processing;
- production monitoring.

## Immediate next actions

1. Introduce Docker terminology and the image-container relationship.
2. Create a PostgreSQL Docker image configuration without replacing or damaging the current local database.
3. Add Docker Compose to define PostgreSQL and supporting services declaratively.
4. Use named volumes for persistent database data.
5. Add environment-variable configuration and health checks.
6. Connect the existing Python and dbt workflows to the containerized PostgreSQL service.
7. Verify repeatable startup, shutdown, rebuild, and data persistence behavior.
8. Add automated CI only after the local containerized workflow is stable.

## Current implementation boundary

The completed implementation covers environment setup, secure local configuration, database connectivity, real-source acquisition, detailed profiling, raw landing, typed validation, accepted and rejected outcomes, transactional bulk loading, deterministic reruns, row-count reconciliation, synthetic test fixtures, automated tests, lint configuration, a persistent pipeline-run audit table, and a tested and documented dbt analytics layer.

No containerized service, scheduled workflow, cloud resource, distributed pipeline, or machine-learning system has been completed yet.

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
