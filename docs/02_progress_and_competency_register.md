# Progress and Competency Register

## Purpose

This register distinguishes exposure from mastery. A concept is not considered learned simply because it has been mentioned or used in one example.

## Status definitions

| Status | Meaning |
|---|---|
| Not started | The concept has not been introduced. |
| Previewed | The concept appeared early to answer a question, but its formal lesson is deferred. |
| Introduced | The basic definition and purpose have been explained. |
| Explained | The concept has been explained clearly enough to be used as current knowledge, although practical evidence may still be missing. |
| Guided practice | The learner has used the concept successfully with step-by-step support. |
| Independent practice | The learner can solve unfamiliar exercises without step-by-step guidance. |
| Applied | The concept has been used correctly in the integrated project. |
| Reviewed | The concept has been revisited after a delay and retained. |
| Portfolio-ready | The implementation and documentation are professionally presentable. |

## Evidence rule

A status upgrade should be supported by evidence such as:

- a written explanation
- a completed exercise
- a correct SQL script
- a test
- a project implementation
- a documented design decision
- a review exercise completed after time has passed

Exploratory work does not need to become a repository artifact. Repository inclusion is a separate decision from learning evidence.

## Programme status

| Phase | Status | Current evidence |
|---|---|---|
| SQL and relational databases | Guided practice | Main relational concepts and practical SQL foundation completed interactively in PostgreSQL and pgAdmin; independent review and portfolio implementation remain |
| Data modelling | Not started | Foundational normalization and operational-versus-analytical distinctions were introduced during SQL, but the dedicated modelling phase has not started |
| ETL, ELT, and pipelines | Introduced | Transition established, initial tooling approach discussed, and implementation not yet started |
| Warehouses, lakes, Snowflake, and dbt | Not started | Roadmap only |
| Workflow orchestration | Not started | Roadmap only |
| APIs, Docker, and CI/CD | Not started | Roadmap only |
| MLOps and MLflow | Not started | Roadmap only |
| Azure and cloud | Not started | Roadmap only |
| NoSQL and specialized data stores | Introduced | Introductory relational-versus-non-relational comparison completed; dedicated roadmap created |
| Spark and Databricks | Not started | Roadmap only |
| Kafka and streaming | Not started | Roadmap only |
| Production infrastructure | Not started | Roadmap only |
| Integrated system | Not started | Initial architecture only |

## SQL foundations status

| Competency | Status | Notes |
|---|---|---|
| Explain why relational databases exist | Explained | Discussed persistence, shared access, consistency, integrity, and trade-offs with denormalized alternatives |
| Distinguish a database from a DBMS | Explained | PostgreSQL identified as the DBMS; `telecom_operations` is a database managed by it |
| Distinguish server, client, and connection | Guided practice | Local PostgreSQL service and pgAdmin connection used successfully |
| Define schema, table, row, and column | Guided practice | `operational` and `analytics` schemas and small tables created locally |
| Define primary key | Guided practice | Primary keys created and constraint behavior inspected |
| Define foreign key | Guided practice | Invoice-to-customer foreign key created, dropped, corrected, and recreated |
| Explain referential integrity | Guided practice | Invalid references and foreign-key behavior discussed and tested conceptually |
| Identify one-to-many relationships | Guided practice | Customer-to-invoice relationship used throughout queries and schema work |
| Identify many-to-many relationships | Explained | Junction-table structure explained; full practical implementation deferred |
| Identify row grain | Guided practice | Customer, invoice, joined, grouped, and analytical grains stated repeatedly |
| Explain `SELECT` and `FROM` | Guided practice | Used throughout interactive PostgreSQL queries |
| Filter rows with `WHERE` | Guided practice | Comparison operators, logical operators, ranges, lists, patterns, dates, and missing values used |
| Work correctly with `NULL` | Guided practice | `IS NULL`, `IS NOT NULL`, `COALESCE`, three-valued logic, and `NOT IN` risks explained |
| Sort and limit results | Guided practice | `ORDER BY`, multiple sort keys, null placement, and `LIMIT` used |
| Use aggregate functions | Guided practice | `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, conditional aggregation, and aggregate `FILTER` explained |
| Use `GROUP BY` and `HAVING` | Guided practice | Group grain and filtering before versus after aggregation explained and used |
| Use conditional expressions | Guided practice | `CASE` and conditional aggregation used |
| Use joins safely | Guided practice | `INNER JOIN`, `LEFT JOIN`, `CROSS JOIN`, and `ON` versus `WHERE` explained and used |
| Diagnose join multiplication | Guided practice | Missing relationship conditions, Cartesian multiplication, and output grain diagnosed interactively |
| Use anti-joins | Guided practice | `LEFT JOIN ... IS NULL` and `NOT EXISTS` explained |
| Use subqueries | Guided practice | Scalar, set-returning, and correlated subqueries explained and used |
| Use `EXISTS` and `NOT EXISTS` | Guided practice | Correlation and the purpose of `SELECT 1` revisited until clear |
| Use common table expressions | Guided practice | Single and multiple CTEs explained; advanced recursion deferred |
| Use set operations | Guided practice | `UNION`, `UNION ALL`, `INTERSECT`, and `EXCEPT` explained and compared with `OR` logic |
| Use window functions | Guided practice | Partitioned aggregates, ranking, running totals, `LAG`, and `LEAD` explained |
| Use text, numeric, and date expressions | Guided practice | Text functions, casting, arithmetic, safe division, intervals, `EXTRACT`, and `DATE_TRUNC` covered |
| Create databases and schemas | Guided practice | `telecom_operations`, `operational`, and `analytics` created locally |
| Create tables with appropriate data types | Guided practice | Customer and invoice tables created; numeric precision error diagnosed and corrected |
| Apply constraints | Guided practice | Primary key, foreign key, `NOT NULL`, `CHECK`, numeric precision, and defaults discussed |
| Modify existing schema objects | Guided practice | `ALTER TABLE`, adding columns, renaming columns, changing types, and changing constraints used |
| Insert, update, and delete rows safely | Guided practice | Explicit columns, `RETURNING`, preview-before-write, and missing-`WHERE` risks explained |
| Use upserts | Explained | `ON CONFLICT`, `DO NOTHING`, `DO UPDATE`, and `EXCLUDED` explained; independent practice pending |
| Use transactions | Guided practice | `BEGIN`, `COMMIT`, `ROLLBACK`, failed transaction state, and savepoints explained |
| Explain ACID properties | Explained | Atomicity, consistency, isolation, and durability connected to pipeline loads |
| Use views and temporary structures | Guided practice | Views, materialized views, CTEs, temporary tables, and permanent tables compared |
| Explain indexes and query plans | Guided practice | B-tree and composite indexes, selectivity, `EXPLAIN`, `EXPLAIN ANALYZE`, and scan types introduced |
| Explain normalization and denormalization | Explained | Normal forms, anomalies, historical snapshots, duplicated mutable facts, and practical trade-offs discussed |
| Normalize a small operational schema | Guided practice | Customers and invoices separated at clear grains with a foreign-key relationship |
| Distinguish operational and analytical tables | Explained | Source-of-truth operational data and derived analytical summaries compared |
| Build a customer-level analytical table | Explained | Full-refresh SQL pattern and validation checks explained; no repository implementation preserved yet |
| Construct a leakage-safe point-in-time modelling table | Not started | Requires the dedicated data-modelling phase and a defined prediction problem |
| Complete an independent mixed SQL assessment | Not started | Required before upgrading the SQL phase to independent practice |
| Produce a portfolio-ready SQL implementation | Not started | Repository inclusion will be decided deliberately when a coherent component exists |

## Relational and non-relational storage status

| Competency | Status | Notes |
|---|---|---|
| Distinguish relational from non-relational databases | Explained | Relational, document, key-value, wide-column, and graph models compared at a high level |
| Explain that NoSQL is an umbrella term | Explained | NoSQL treated as multiple model families rather than one database type |
| Explain document databases | Introduced | Nested customer-and-services example discussed |
| Explain key-value databases | Introduced | Cache and session examples discussed |
| Explain wide-column databases | Introduced | Large distributed write workloads mentioned |
| Explain graph databases | Introduced | Nodes, relationships, and traversal-oriented workloads introduced |
| Compare normalization, denormalization, and embedding | Explained | Trade-offs, application-side synchronization, historical snapshots, and derived stores discussed |
| Explain polyglot persistence | Introduced | Multiple database types used for different workloads |
| Explain consistency and replication trade-offs | Not started | Dedicated roadmap topic |
| Select a storage model from workload requirements | Not started | Requires comparative exercises and implementation evidence |
| Implement a document database | Not started | Deferred until specialized-data-store phase |
| Implement a key-value database | Not started | Deferred until specialized-data-store phase |
| Implement a graph database | Not started | Deferred until specialized-data-store phase |

## Practical tooling status

| Tool or skill | Status | Notes |
|---|---|---|
| PostgreSQL | Guided practice | PostgreSQL 18 installed and used through a local learning database |
| pgAdmin 4 | Guided practice | Query Tool, Object Explorer, constraints, columns, and query results used |
| `psql` | Not started | Command-line client remains deferred |
| SQL files in version control | Not started | Interactive SQL exercises were intentionally not converted automatically into repository deliverables |
| Python environment for ETL | Not started | Version verification and virtual environment creation are the next practical setup steps |
| Python database connection | Not started | Psycopg approach selected conceptually; implementation pending |
| Automated pipeline tests | Not started | Planned after the first transparent pipeline works |
| Logging and configuration | Not started | Planned during ETL implementation |
| MongoDB or equivalent document store | Not started | Deferred to specialized data stores roadmap |
| Redis or equivalent key-value store | Not started | Deferred to specialized data stores roadmap |
| Neo4j or equivalent graph store | Not started | Deferred to specialized data stores roadmap |
| Dockerized PostgreSQL | Not started | Deferred until Docker foundations |
| Cloud database | Not started | Deferred until Azure phase |

## Current evidence boundary

The SQL checkpoint supports moving into ETL, but the following evidence is still absent:

- a delayed review of the SQL material
- a mixed independent SQL assessment
- a complete point-in-time analytical dataset
- a version-controlled SQL implementation selected for portfolio use
- automated database tests
- an integrated production project application

These gaps should not block the ETL learning phase. They should prevent premature claims of independent mastery or portfolio readiness.

## Review cadence

At the end of each major part:

1. complete a mixed independent exercise set
2. explain the main concepts without looking at notes
3. apply selected concepts to a coherent implementation
4. record mistakes and corrections
5. schedule a later review before changing status to `Reviewed`
