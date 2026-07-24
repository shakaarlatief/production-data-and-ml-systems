# Current Status and Next Actions

## Repository purpose

This repository is a separate learning and portfolio programme for production data and machine-learning systems. It is not part of the Telco Customer Churn classification repository.

## Active phase

**Phase 3: ETL, ELT, and data pipelines**

The SQL and relational-database foundation has reached the checkpoint needed to begin pipeline work. This does not mean that every advanced PostgreSQL topic has been completed or independently mastered. It means that the required concepts for understanding extraction, transformation, loading, transactions, validation, and database-backed pipelines have been introduced and practised sufficiently to continue.

## Active lesson

**ETL foundations and local development preparation**

The immediate objective is to understand how a pipeline moves data between sources and targets, then prepare a small local Python-to-PostgreSQL workflow. The first implementation should expose each step clearly before higher-level frameworks are introduced.

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
- The `telecom_operations` database exists.
- The `operational` and `analytics` schemas exist.
- Small `customers` and `invoices` tables have been created and queried.
- Constraints, foreign keys, data types, transactions, views, and indexes have been explored interactively.

## Evidence boundary

The SQL phase was primarily a learning and guided-practice phase. Interactive statements executed in pgAdmin were not automatically treated as repository deliverables.

The current evidence supports conceptual understanding and guided use of the main SQL and relational-database topics. It does not yet support claims that every topic has been independently applied, reviewed after a delay, or implemented as a portfolio-ready database project.

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

1. Introduce extraction, transformation, loading, ETL versus ELT, batch processing, and pipeline stages.
2. Explain full refresh, incremental loading, idempotency, checkpoints, and watermarks.
3. Verify the existing Python installation and create a local virtual environment when implementation begins.
4. Install only the initial packages needed for a transparent local Python-to-PostgreSQL example.
5. Build a small exploratory pipeline that extracts data, applies explicit transformations, validates the result, and loads it transactionally.
6. Decide during development which parts are worth preserving in the repository.
7. Add testing, logging, configuration, and failure handling after the first transparent pipeline works.

## Current implementation boundary

A local PostgreSQL learning database exists and has been used interactively. No Python ETL pipeline, scheduled workflow, cloud resource, or production application has been implemented yet.

The repository currently remains primarily a planning and progress-tracking repository. ETL code and supporting project structure should be added only when a coherent implementation is ready to preserve.

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
