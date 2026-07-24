# Current Status and Next Actions

## Repository purpose

This repository is a separate learning and portfolio programme for production data and machine-learning systems. It is not part of the Telco Customer Churn classification repository.

## Active phase

**Phase 3: ETL, ELT, and data pipelines**

The SQL and relational-database foundation has reached the checkpoint needed to begin pipeline work. This does not mean that every advanced PostgreSQL topic has been completed or independently mastered. It means that the required concepts for understanding extraction, transformation, loading, transactions, validation, and database-backed pipelines have been introduced and practised sufficiently to continue.

## Active lesson

**Real-file extraction, source profiling, and staging-table design**

The first practical ETL case study uses official January 2025 Jersey City Citi Bike trip-history data. The immediate objective is to profile the real source carefully, convert the observed source properties into explicit data-quality rules, and design the first PostgreSQL staging layer before loading records.

The implementation remains intentionally transparent. Direct Python, the standard library, Psycopg 3, PostgreSQL, and explicit SQL are used before introducing higher-level data-processing, orchestration, warehouse, container, or cloud abstractions.

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
- The extracted source file has been inspected with Python.

## Initial source evidence

The first source file is:

`JC-202501-citibike-tripdata.csv`

Observed grain:

`one row per recorded bicycle ride`

Observed structure:

- 50,611 data rows
- 13 columns
- ride identifiers, bicycle type, start and end timestamps, start and end station information, coordinates, and membership category

Observed missingness:

| Column | Missing rows | Missing percentage |
|---|---:|---:|
| `end_station_name` | 107 | 0.21% |
| `end_station_id` | 132 | 0.26% |
| `end_lat` | 19 | 0.04% |
| `end_lng` | 19 | 0.04% |

No missing values were observed in the other columns during the initial inspection.

## Evidence boundary

The SQL phase was primarily a learning and guided-practice phase. Interactive statements executed in pgAdmin were not automatically treated as repository deliverables.

The current ETL evidence now includes a functioning local Python environment, a verified PostgreSQL connection, a dedicated database, initial schema separation, reproducible access to a real public source file, and a source-inspection program. This does not yet support claims that a complete ETL pipeline, transactional batch load, rejection workflow, idempotent rerun mechanism, automated test suite, or scheduled workflow exists.

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

1. Profile ride identifiers, categorical values, timestamps, coordinates, duration behavior, and duplicate rows.
2. Decide which source properties are contractual requirements and which are observed but not guaranteed.
3. Define explicit validation rules and rejected-record reasons.
4. Design the first staging table from the evidence rather than from assumptions.
5. Implement extraction and parsing functions that preserve the raw source file.
6. Load the first batch transactionally into PostgreSQL.
7. Reconcile source, valid, rejected, and loaded row counts.
8. Make reruns safe and deterministic.
9. Add logging, tests, and configuration validation after the first transparent load works.
10. Decide which implementation files form the first coherent repository milestone.

## Current implementation boundary

The repository now contains the beginning of a local ETL implementation rather than planning documents alone. The completed work covers environment setup, secure local configuration, database connectivity, real-source acquisition, and initial source inspection.

No production-ready ETL package, final relational model, scheduled workflow, cloud resource, containerized service, or machine-learning pipeline has been completed yet.

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
