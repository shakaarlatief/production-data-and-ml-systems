# Production Data and ML Systems

This repository is a structured learning and portfolio project for building the knowledge required to move from local Python or R analysis toward professional data, cloud, and machine-learning systems.

It is separate from the Telco Customer Churn classification project. The purpose here is not primarily to compare predictive models. The purpose is to understand and implement the surrounding systems that organizations use to collect, store, transform, schedule, deploy, monitor, and maintain data and machine-learning workloads.

## Learning scope

The programme covers:

1. SQL and relational databases
2. Data modelling and analytical dataset construction
3. ETL, ELT, and data pipelines
4. Data warehouses, data lakes, lakehouses, Snowflake, and dbt
5. Workflow orchestration
6. APIs, software engineering, Docker, and CI/CD
7. MLOps and MLflow
8. Azure and cloud infrastructure
9. Distributed processing with Spark and Databricks
10. Streaming systems with Kafka
11. Kubernetes, Terraform, security, monitoring, and production operations
12. An integrated end-to-end production project

## Learning philosophy

The repository follows several principles:

- Concepts are learned in dependency order.
- Technologies are introduced as solutions to concrete problems, not as isolated product names.
- Every new keyword, function, symbol, and piece of syntax is explained before it is relied on.
- Small examples are used before larger implementations.
- Input data, transformations, output data, and row grain are made explicit.
- Theory, guided exercises, independent exercises, and project application are tracked separately.
- Local implementations are developed before equivalent cloud implementations where possible.
- Documentation is written as a standalone technical reference that can be revisited later.

## Repository documentation

The main planning and coordination documents are located in `docs/`:

- `00_master_learning_map.md`: complete programme and dependency order
- `01_current_status_and_next_actions.md`: active phase, current lesson, and immediate work
- `02_progress_and_competency_register.md`: skill status and evidence of mastery
- `03_integrated_project_architecture.md`: evolving end-to-end system design
- `04_technology_decision_register.md`: technology choices and alternatives
- `05_glossary.md`: definitions and distinctions between related terms
- `06_documentation_workflow.md`: documentation roles and update rules
- `roadmaps/`: detailed roadmap for each major subject area

## Current phase

The active phase is SQL and relational databases. The first objective is to build a rigorous foundation in relational data, PostgreSQL, SQL querying, data integrity, database design, and the construction of analytical and machine-learning datasets from normalized operational tables.

## Intended result

The long-term result will be a professional, portfolio-ready system that demonstrates how data moves from operational sources through storage, transformation, orchestration, machine-learning training, deployment, monitoring, and retraining.
