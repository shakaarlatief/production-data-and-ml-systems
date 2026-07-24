# Current Status and Next Actions

## Repository purpose

This repository is a separate learning and portfolio programme for production data and machine-learning systems. It is not part of the Telco Customer Churn classification repository.

## Active phase

**Phase 3: ETL, ELT, and data pipelines**

The SQL and relational-database foundation has reached the checkpoint needed to continue pipeline work. The active implementation uses direct Python, the standard library, Psycopg 3, PostgreSQL, and explicit SQL so that each responsibility remains visible before higher-level transformation, orchestration, container, distributed-processing, or cloud abstractions are introduced.

## Active lesson

**dbt Core and analytics-layer design**

The Citi Bike case study now has:

- a reproducible raw landing layer;
- a typed accepted-record and rejected-record staging layer;
- deterministic rerun behavior;
- source-to-database reconciliation;
- controlled synthetic validation fixtures;
- automated unit tests;
- reproducible Python dependency and quality-tool configuration;
- a persistent PostgreSQL table for pipeline-run audit records.

The immediate objective is to introduce dbt Core as the first dedicated analytics-engineering tool, connect it to the existing PostgreSQL database, define the validated staging data as a dbt source, and build tested analytical models without expanding the bicycle-domain analysis unnecessarily.

## Practical environment

- PostgreSQL 18 is installed locally and running.
- pgAdmin 4 is connected to the local PostgreSQL server.
- A Python 3.11 virtual environment is used for this repository.
- Local credentials are loaded from an ignored `.env` file.
- A dedicated `bike_share_etl` database is available.
- The `source`, `staging`, `analytics`, and `operations` schemas exist inside `bike_share_etl`.
- The official January 2025 Jersey City Citi Bike file is stored locally under ignored raw-data storage.
- The repository is installable in editable mode through `pyproject.toml`.
- Pytest and Ruff are available through the optional `dev` dependency group.

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

## Automated validation evidence completed

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

## Reproducible Python project configuration

`pyproject.toml` records:

- the supported Python version;
- runtime dependencies;
- optional development dependencies;
- package discovery under `src/`;
- pytest configuration;
- Ruff configuration.

The package is installed locally with:

```bash
python -m pip install -e ".[dev]"
```

Generated `*.egg-info/` package metadata is excluded from version control.

## Evidence boundary

Evidence supports claims that the case study includes:

- real-file profiling;
- reproducible raw, staging, and operations table definitions;
- transactional raw ingestion;
- SHA-256-based idempotency;
- typed validation;
- explicit accepted and rejected outcomes;
- hard rules and soft quality flags;
- deterministic enrichment with source-value preservation;
- raw-to-staging reconciliation;
- rerun-safe staging replacement;
- controlled synthetic test fixtures;
- automated unit tests;
- repeatable lint and test commands;
- a verified pipeline-run audit table structure.

Evidence does not yet support claims that the repository includes:

- automatic pipeline-run audit writes;
- structured production logging;
- centralized shared configuration and database utilities;
- dbt-managed analytical models;
- orchestration;
- containerization;
- cloud deployment;
- distributed processing;
- production monitoring.

## Immediate next actions

1. Install the PostgreSQL adapter for dbt Core in the existing Python 3.11 environment.
2. Create a dbt project inside the repository with generated output excluded from Git.
3. Configure a local PostgreSQL target using environment variables rather than committed credentials.
4. Define `staging.citibike_trip_valid` and related tables as dbt sources.
5. Build the first analytics-layer models with explicit grains.
6. Add dbt data tests, source tests, descriptions, and generated documentation.
7. Compare dbt-managed SQL transformations with the earlier manual Python and SQL implementation.
8. Return later to automatic run auditing, structured logging, orchestration, and continuous integration.

## Current implementation boundary

The completed implementation covers environment setup, secure local configuration, database connectivity, real-source acquisition, detailed profiling, raw landing, typed validation, accepted and rejected outcomes, transactional bulk loading, deterministic reruns, row-count reconciliation, synthetic test fixtures, automated tests, lint configuration, and a persistent pipeline-run audit table definition verified in PostgreSQL.

No dbt-managed analytical model, scheduled workflow, cloud resource, containerized service, distributed pipeline, or machine-learning system has been completed yet.

## Deferred until prerequisites are ready

- advanced PostgreSQL administration;
- recursive CTEs;
- triggers and stored procedures;
- deep transaction-isolation and locking analysis;
- partitioning and advanced index types;
- Airflow or another orchestrator;
- Docker;
- MLflow;
- Azure;
- NoSQL implementations;
- Spark;
- Kafka;
- Kubernetes;
- Terraform.

## Update rule

This document is the tactical source of truth. It should be updated whenever the active lesson, immediate next action, implementation boundary, or repository inclusion decision changes.
