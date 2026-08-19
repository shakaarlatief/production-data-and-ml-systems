# Production Data and ML Systems

A structured learning and portfolio project focused on the engineering required to move from local Python or R analysis toward professional data, cloud, and machine-learning systems.

The project is deliberately built in dependency order. Technologies are introduced as solutions to concrete engineering problems and are applied in small implementations before the scope expands to larger production systems.

## Current implementation

The practical case study currently uses official Citi Bike trip-history data to build a reproducible batch data pipeline. The implemented system includes:

- Python-based source profiling, ingestion, and validation;
- PostgreSQL raw, staging, operations, and analytics layers;
- SHA-256 file registration and rerun-safe ingestion;
- explicit accepted and rejected validation outcomes;
- raw-to-staging reconciliation and data-quality checks;
- automated Python unit tests and Ruff checks;
- a persistent pipeline-run audit-table design;
- a dbt Core analytics project with declared sources, staging models, marts, generic tests, singular tests, documentation, and lineage;
- a Docker Compose PostgreSQL environment with persistent storage, health checks, environment-based configuration, and automatic foundational-schema initialization.

The current infrastructure milestone is containerizing the Python and dbt execution environment so the full workflow can run without depending on host-installed Python packages.

## Current stack

- Python 3.11
- PostgreSQL 18
- Psycopg 3
- SQL
- dbt Core
- Docker and Docker Compose
- Pytest
- Ruff

## Architecture developed so far

```text
source file
    |
    v
source.citibike_file
source.citibike_trip_raw
    |
    v
staging.citibike_trip_valid
staging.citibike_trip_rejected
    |
    v
dbt staging view
    |
    v
analytics.daily_citibike_activity
```

The implementation keeps the grain and responsibility of each layer explicit. Raw source values are preserved, validation produces typed accepted or rejected outcomes, analytical transformations are handled separately, and reconciliation checks verify that records are not silently lost between stages.

## Broader learning scope

The repository is also the roadmap for a larger end-to-end production learning programme covering:

1. SQL and relational databases
2. Data modelling and analytical dataset construction
3. ETL, ELT, and data pipelines
4. Data warehouses, data lakes, lakehouses, Snowflake, and dbt
5. Workflow orchestration
6. APIs, software engineering, Docker, and CI/CD
7. MLOps and MLflow
8. Azure and cloud infrastructure
9. NoSQL and specialized data stores
10. Distributed processing with Spark and Databricks
11. Streaming systems with Kafka
12. Kubernetes, Terraform, security, monitoring, and production operations
13. An integrated end-to-end production project

## Learning and engineering principles

The project follows several principles:

- Concepts are learned in dependency order.
- Technologies are introduced as solutions to concrete problems rather than as isolated product names.
- Input data, transformations, output data, and row grain are made explicit.
- Small examples precede larger implementations.
- Theory, guided work, independent work, and project application are tracked separately.
- Local implementations are developed before equivalent cloud implementations where useful.
- Storage technologies are selected from workload requirements rather than from a relational-versus-NoSQL slogan.
- Documentation is written as a standalone technical reference that can be revisited later.
- Repository artifacts are selected deliberately when they form a reusable implementation, meaningful milestone, polished example, or part of the integrated system.

## Repository documentation

The main planning and technical documents are located in `docs/`:

- `00_master_learning_map.md`: complete programme and dependency order
- `01_current_status_and_next_actions.md`: active phase, current lesson, and immediate work
- `02_progress_and_competency_register.md`: skill status and evidence of mastery
- `03_integrated_project_architecture.md`: evolving end-to-end system design
- `04_technology_decision_register.md`: technology choices and alternatives
- `05_glossary.md`: definitions and distinctions between related terms
- `06_documentation_workflow.md`: documentation roles and update rules
- `07_industry_tooling_landscape.md`: industry-facing map of tools, priorities, alternatives, and planned learning phases
- `08_citibike_etl_case_study.md`: detailed practical ETL case study
- `09_docker_compose_postgresql.md`: containerized PostgreSQL milestone
- `roadmaps/`: detailed roadmap for each major subject area

## Intended result

The long-term goal is a professional, portfolio-ready system that demonstrates how data moves from operational sources through storage, transformation, orchestration, machine-learning training, deployment, monitoring, and retraining, while documenting the design choices and trade-offs along the way.
