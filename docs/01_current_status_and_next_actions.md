# Current Status and Next Actions

## Repository purpose

This repository is a separate learning and portfolio programme for production data and machine-learning systems. It is not part of the Telco Customer Churn classification repository.

## Active phase

**Phase 3: ETL, ELT, and data pipelines**

The SQL and relational-database foundation has reached the checkpoint needed to continue pipeline work. This does not mean that every advanced PostgreSQL topic has been completed or independently mastered. It means that the required concepts for understanding extraction, transformation, loading, transactions, validation, and database-backed pipelines have been introduced and practised sufficiently to continue.

## Active lesson

**Automated validation, pipeline observability, and analytics-layer design**

The first practical ETL case study now has a functioning raw landing layer and a validated staging layer built from official January 2025 Jersey City Citi Bike trip-history data.

The immediate objective is to strengthen the pipeline through controlled tests, structured logging, reusable configuration, and an explicit analytics-layer model. The implementation remains intentionally transparent: direct Python, the standard library, Psycopg 3, PostgreSQL, and explicit SQL are used before higher-level orchestration, warehouse, container, or cloud abstractions are introduced.

## SQL checkpoint reached

The following areas have been explained and, in many cases, practised interactively in PostgreSQL and pgAdmin:

- PostgreSQL server, client, connection, database, schema, table, row, column, and data type
- row grain, entities, attributes, primary keys, foreign keys, and referential integrity
- one-to-one, one-to-many, and many-to-many relationships
- relational versus non-relational database models at an introductory level
- `SELECT`, aliases, expressions, filtering, sorting, limiting, and `DISTINCT`
- missing-value handling and SQL three-valued logic
- aggregate functions, `GROUP BY`, `HAVING`, and conditional aggregation
- `INNER JOIN`, `LEFT JOIN`, `CROSS JOIN`, join conditions, row multiplication, and anti-joins
- subqueries, correlated subqueries, `IN`, `EXISTS`, `NOT EXISTS`, and common table expressions
- window functions, partitioning, ranking, running totals, `LAG`, and `LEAD`
- `UNION`, `UNION ALL`, `INTERSECT`, and `EXCEPT`
- text functions, casting, arithmetic, date arithmetic, `EXTRACT`, `DATE_TRUNC`, and intervals
- `INSERT`, `UPDATE`, `DELETE`, `RETURNING`, `INSERT ... SELECT`, and upserts
- transactions, rollback, savepoints, and the ACID properties
- views, materialized views, temporary tables, and permanent tables
- indexes, composite index order, `EXPLAIN`, `EXPLAIN ANALYZE`, and planner statistics
- normalization, denormalization, insertion, update, and deletion anomalies
- operational versus analytical table design and a simple SQL-to-ETL bridge

## Practical environment completed

- PostgreSQL 18 is installed locally and running.
- pgAdmin 4 is connected to the local PostgreSQL server.
- The earlier `telecom_operations` learning database remains available for SQL practice.
- A Python 3.11 virtual environment has been created for this repository.
- Psycopg 3 and python-dotenv have been installed in the virtual environment.
- Local database credentials are loaded from an ignored `.env` file.
- Python-to-PostgreSQL connectivity has been verified successfully.
- A dedicated `bike_share_etl` database has been created.
- The `source`, `staging`, and `analytics` schemas have been created inside `bike_share_etl`.
- The official January 2025 Jersey City Citi Bike trip-history archive has been downloaded locally.
- Raw data under `data/raw/` is excluded from Git.

## Source evidence

The first source file is:

`JC-202501-citibike-tripdata.csv`

Observed grain:

`one row per recorded bicycle ride`

Observed structure:

- 50,611 data rows
- 13 columns
- ride identifiers, bicycle type, start and end timestamps, start and end station information, coordinates, and membership category

Key profiling results:

- all 50,611 ride identifiers are unique
- no exact duplicate rows were found
- all timestamps parse successfully
- no nonpositive trip durations were found
- 21 trips exceed 24 hours
- 25 missing end-station identifiers can be inferred uniquely from station names
- 107 rows remain without a resolved end station
- 19 rows have no end coordinates
- all non-missing coordinates are finite and geographically valid
- station identifier `JC075` appears with two name variants

## Raw landing layer completed

The repository now contains reproducible raw-layer DDL and a transactional ingestion program.

Implemented tables:

- `source.citibike_file`
- `source.citibike_trip_raw`

Implemented behavior:

- SHA-256 file identity
- source-file manifest metadata
- immutable raw source values stored as text
- source-row lineage through `(file_id, source_row_number)`
- bulk loading through PostgreSQL `COPY`
- transactional rollback behavior
- source-to-database row-count reconciliation
- idempotent rerun handling

Observed result:

| Measure | Count |
|---|---:|
| Manifest source rows | 50,611 |
| Raw database rows | 50,611 |
| Second-run duplicate rows inserted | 0 |

## Validated staging layer completed

Implemented tables:

- `staging.citibike_trip_valid`
- `staging.citibike_trip_rejected`

The validation program parses timestamps and coordinates, checks required values and accepted categories, calculates trip duration, separates hard rejection rules from soft quality conditions, preserves source lineage, and distinguishes provider-supplied station identifiers from deterministically inferred identifiers.

Observed result from two identical validation executions:

| Measure | Count |
|---|---:|
| Raw rows | 50,611 |
| Valid rows | 50,611 |
| Rejected rows | 0 |
| Reconciliation | 50,611 + 0 = 50,611 |

Observed quality flags among accepted rows:

| Quality flag | Count |
|---|---:|
| Missing resolved end station | 107 |
| End-station identifier inferred from station name | 25 |
| Trip longer than 24 hours | 21 |
| Missing end coordinates | 19 |

The second execution reproduced the same result without appending duplicate staging rows.

## Evidence boundary

The repository now contains a functioning local batch ETL foundation rather than planning documents alone.

Evidence supports claims that the case study includes:

- real-file source profiling
- reproducible PostgreSQL raw-table creation
- transactional raw ingestion
- SHA-256-based idempotent reruns
- explicit valid and rejected staging outcomes
- hard validation rules and soft quality flags
- deterministic source-value enrichment with lineage preservation
- raw-to-staging reconciliation
- rerun-safe staging replacement for one file

Evidence does not yet support claims that the repository includes:

- comprehensive automated tests
- structured production logging
- persistent pipeline-run metadata
- a completed analytical model
- orchestration
- containerization
- cloud deployment
- distributed processing
- production monitoring

## Repository inclusion rule

Exploratory code, exercises, and temporary experiments are not added to the repository automatically.

A repository artifact is added only after a deliberate decision that it is useful as one of the following:

- a reusable implementation
- a meaningful project milestone
- a polished technical example
- documentation worth preserving
- part of the eventual integrated system

This rule applies to SQL, ETL, and all later phases.

## Immediate next actions

1. Add controlled synthetic fixtures for each hard rejection rule.
2. Add automated tests for parsing, validation, reconciliation, and rerun behavior.
3. Add structured logging and a persistent pipeline-run table.
4. Centralize shared path, environment, and database-connection logic.
5. Design analytical trip and station models with explicit grains.
6. Build the first analytics-layer transformation from validated records.
7. Add a second monthly file to test cross-file uniqueness and multi-file processing.
8. Introduce reproducible dependency metadata, formatting, linting, and test commands.

## Current implementation boundary

The completed implementation covers environment setup, secure local configuration, database connectivity, real-source acquisition, detailed source profiling, raw landing, typed validation, accepted and rejected outcomes, transactional bulk loading, deterministic reruns, and row-count reconciliation.

No production-ready package, final analytical model, scheduled workflow, cloud resource, containerized service, distributed pipeline, or machine-learning system has been completed yet.

## Deferred until prerequisites are ready

- advanced PostgreSQL administration
- recursive CTEs
- triggers and stored procedures
- deep transaction-isolation and locking analysis
- partitioning and advanced index types
- dbt
- Airflow or another orchestrator
- Docker
- MLflow
- Azure
- NoSQL implementations
- Spark
- Kafka
- Kubernetes
- Terraform

## Update rule

This document is the tactical source of truth. It should be updated whenever the active lesson, immediate next action, implementation boundary, or repository inclusion decision changes.
