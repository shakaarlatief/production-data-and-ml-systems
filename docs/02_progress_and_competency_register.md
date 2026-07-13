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

## Programme status

| Phase | Status | Current evidence |
|---|---|---|
| SQL and relational databases | Introduced | Relational foundations and basic query syntax discussed; detailed roadmap created |
| Data modelling | Not started | Roadmap only |
| ETL, ELT, and pipelines | Not started | Roadmap only |
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
| Explain why relational databases exist | Explained | Discussed using customers, invoices, consistency, shared access, and integrity |
| Distinguish a database from a DBMS | Explained | PostgreSQL identified as the DBMS rather than the database itself |
| Distinguish server, client, and connection | Explained | Local PostgreSQL and pgAdmin architecture introduced |
| Define schema, table, row, and column | Explained | Formal practical use still required |
| Define primary key | Explained | Formal exercises still required |
| Define foreign key | Explained | Formal exercises still required |
| Explain referential integrity | Explained | Formal exercises still required |
| Identify one-to-many relationships | Explained | Customer-to-invoice example |
| Identify many-to-many relationships | Explained | Customer-to-service junction-table example |
| Identify row grain | Explained | Customer, invoice, payment, and customer-month examples |
| Explain `SELECT` | Explained | Conceptual explanation completed; PostgreSQL execution pending |
| Explain `FROM` | Explained | Conceptual explanation completed; PostgreSQL execution pending |
| Explain `*` in `SELECT *` | Explained | Distinguished from multiplication and from `COUNT(*)` |
| Explain `;` | Explained | Introduced as a statement terminator |
| Explain aliases with `AS` | Explained | Conceptual explanation completed |
| Filter rows with `WHERE` | Not started | Planned after local PostgreSQL setup |
| Work correctly with `NULL` | Not started | |
| Sort and limit results | Not started | |
| Use aggregate functions | Introduced | `COUNT`, `AVG`, `SUM`, and `MAX` explained conceptually; practical queries pending |
| Use `GROUP BY` | Introduced | Grouping and grain change explained; practical queries pending |
| Use joins safely | Not started | |
| Diagnose join multiplication | Not started | |
| Use subqueries and CTEs | Not started | |
| Use window functions | Previewed | `COUNT(*) OVER (PARTITION BY ...)` discussed early |
| Create tables with appropriate data types | Not started | |
| Apply constraints | Not started | |
| Use transactions | Not started | |
| Explain indexes and query plans | Not started | |
| Normalize an operational schema | Not started | |
| Build a customer-level modelling table | Not started | |

## Relational and non-relational storage status

| Competency | Status | Notes |
|---|---|---|
| Distinguish relational from non-relational databases | Introduced | High-level comparison completed |
| Explain that NoSQL is an umbrella term | Introduced | Document, key-value, wide-column, and graph families identified |
| Explain document databases | Introduced | Nested customer-and-services example discussed |
| Explain key-value databases | Introduced | Cache and session examples discussed |
| Explain wide-column databases | Introduced | Large distributed write workloads mentioned |
| Explain graph databases | Introduced | Nodes, relationships, and path-oriented use cases discussed |
| Compare normalization with embedding | Previewed | Formal modelling lesson deferred |
| Explain polyglot persistence | Introduced | Multiple database types used for different workloads |
| Explain consistency and replication trade-offs | Not started | Dedicated roadmap topic |
| Select a storage model from workload requirements | Not started | Requires comparative exercises and implementation evidence |
| Implement a document database | Not started | Deferred until prerequisites are ready |
| Implement a key-value database | Not started | Deferred until prerequisites are ready |
| Implement a graph database | Not started | Deferred until prerequisites are ready |

## Practical tooling status

| Tool or skill | Status | Notes |
|---|---|---|
| PostgreSQL | Not started | Selected as primary local database; installation is next |
| pgAdmin 4 | Not started | Selected for the first local connection |
| `psql` | Not started | Command-line client to be installed with PostgreSQL |
| SQL files in version control | Not started | |
| Python database connection | Not started | |
| Automated SQL tests | Not started | |
| MongoDB or equivalent document store | Not started | Deferred to specialized data stores roadmap |
| Redis or equivalent key-value store | Not started | Deferred to specialized data stores roadmap |
| Neo4j or equivalent graph store | Not started | Deferred to specialized data stores roadmap |
| Dockerized PostgreSQL | Not started | Deferred until Docker foundations |
| Cloud database | Not started | Deferred until Azure phase |

## Review cadence

At the end of each major part:

1. complete a mixed independent exercise set
2. explain the main concepts without looking at notes
3. apply the concepts to the integrated project
4. record mistakes and corrections
5. schedule a later review before changing status to `Reviewed`
