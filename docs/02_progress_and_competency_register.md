# Progress and Competency Register

## Purpose

This register distinguishes exposure from mastery. A concept is not considered learned simply because it has been mentioned or used in one example.

## Status definitions

| Status | Meaning |
|---|---|
| Not started | The concept has not been introduced. |
| Previewed | The concept appeared early to answer a question, but its formal lesson is deferred. |
| Introduced | The basic definition and purpose have been explained. |
| Explained | The learner can explain the concept accurately in their own words. |
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
| SQL and relational databases | Introduced | Initial concepts discussed; detailed roadmap created |
| Data modelling | Not started | Roadmap only |
| ETL, ELT, and pipelines | Not started | Roadmap only |
| Warehouses, lakes, Snowflake, and dbt | Not started | Roadmap only |
| Workflow orchestration | Not started | Roadmap only |
| APIs, Docker, and CI/CD | Not started | Roadmap only |
| MLOps and MLflow | Not started | Roadmap only |
| Azure and cloud | Not started | Roadmap only |
| Spark and Databricks | Not started | Roadmap only |
| Kafka and streaming | Not started | Roadmap only |
| Production infrastructure | Not started | Roadmap only |
| Integrated system | Not started | Initial architecture only |

## SQL foundations status

| Competency | Status | Notes |
|---|---|---|
| Explain why relational databases exist | Introduced | Discussed using customers and invoices |
| Define table, row, and column | Introduced | Formal completion still required |
| Define primary key | Introduced | Formal exercises still required |
| Define foreign key | Introduced | Formal exercises still required |
| Explain referential integrity | Introduced | Formal exercises still required |
| Identify one-to-many relationships | Introduced | Customer to invoice example |
| Identify row grain | Introduced | Invoice-level versus customer-level distinction |
| Explain `SELECT` | Not started | Planned next |
| Explain `FROM` | Not started | Planned next |
| Explain `*` in `SELECT *` | Not started | Planned next |
| Explain `;` | Not started | Planned next |
| Filter rows with `WHERE` | Not started | |
| Work correctly with `NULL` | Not started | |
| Sort and limit results | Not started | |
| Use aggregate functions | Previewed | `COUNT`, `AVG`, `SUM`, and `MAX` discussed early |
| Use `GROUP BY` | Previewed | Difference from row-preserving calculations discussed |
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

## Practical tooling status

| Tool or skill | Status | Notes |
|---|---|---|
| PostgreSQL | Not started | Selected as primary local database |
| Database client | Not started | Selection deferred until installation lesson |
| SQL files in version control | Not started | |
| Python database connection | Not started | |
| Automated SQL tests | Not started | |
| Dockerized PostgreSQL | Not started | Deferred until Docker foundations |
| Cloud database | Not started | Deferred until Azure phase |

## Review cadence

At the end of each major SQL part:

1. complete a mixed independent exercise set
2. explain the main concepts without looking at notes
3. apply the concepts to the telecom database
4. record mistakes and corrections
5. schedule a later review before changing status to `Reviewed`
