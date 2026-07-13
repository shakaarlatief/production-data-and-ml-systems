# Current Status and Next Actions

## Repository purpose

This repository is a separate learning and portfolio programme for production data and machine-learning systems. It is not part of the Telco Customer Churn classification repository.

## Active phase

**Phase 1: SQL and relational databases**

## Active lesson

**PostgreSQL installation and first local connection**

The relational foundations have already been introduced conceptually. The immediate objective is now to install the local tools and connect to a real PostgreSQL server before creating the first project database.

## Concepts already introduced

The following concepts have been explained conceptually, but most have not yet been practised in PostgreSQL:

- database and database management system
- PostgreSQL as a relational database management system
- server, client, and connection
- database, schema, table, row, column, and data type
- entity, attribute, and row grain
- primary, foreign, composite, natural, and surrogate keys
- referential integrity
- one-to-one, one-to-many, and many-to-many relationships
- junction tables
- `SELECT`
- `FROM`
- `*` in `SELECT *`
- semicolon as a statement terminator
- aliases with `AS`
- the context-dependent meaning of `*`
- `COUNT(*)` versus `COUNT(column)`
- aggregate functions including `COUNT`, `AVG`, `SUM`, and `MAX`
- `GROUP BY` and the resulting change in row grain
- the difference between grouped aggregation and row-preserving window calculations
- `OVER` and `PARTITION BY` in an introductory window-function example
- relational versus non-relational database models at an introductory level

## Concepts previewed but not yet completed

The following subjects appeared in introductory discussion but still require formal lessons, guided practice, and independent application:

- aggregate functions in complete SQL queries
- `GROUP BY`
- window functions
- `OVER`
- `PARTITION BY`
- document, key-value, wide-column, and graph databases
- NoSQL consistency, replication, and distributed trade-offs
- selection between relational and specialized data stores

## Completed setup

- repository created
- master learning map established
- detailed topic roadmaps established
- documentation roles established
- progress framework established
- initial architecture and technology decisions recorded
- README created
- NoSQL and specialized data stores added to the programme
- early relational-versus-non-relational comparison added to the SQL roadmap

## Immediate next actions

1. Install PostgreSQL Server, pgAdmin 4, and the PostgreSQL command-line tools.
2. Verify that the local PostgreSQL server is running.
3. Connect through pgAdmin using `localhost` and port `5432`.
4. Confirm access to the default `postgres` database.
5. Create the first telecom learning database.
6. Create small `customers` and `invoices` tables.
7. Execute the already-explained basic `SELECT` queries against real tables.
8. Continue with filtering through `WHERE` and comparison operators.
9. Add the first detailed knowledge note under `docs/knowledge_notes/sql/`.
10. Update the competency register only when additional evidence is produced.

## Current implementation boundary

No project database, pipeline, cloud service, or production application has been implemented yet. The current repository contains planning and conceptual documentation. PostgreSQL installation is the next practical implementation step.

## Deferred until prerequisites are ready

- formal aggregation exercises
- joins
- window-function exercises
- analytical schema design
- hands-on NoSQL implementations
- dbt
- Airflow
- Docker
- MLflow
- Azure
- Spark
- Kafka
- Kubernetes
- Terraform

## Update rule

This document is the tactical source of truth. It should be updated whenever the active lesson, immediate next action, or implementation boundary changes.
