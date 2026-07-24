# Industry Tooling Landscape

## Purpose

This document maps important tools that appear across data engineering, analytics engineering, data science, machine-learning engineering, MLOps, cloud, and production-platform work.

It is not a checklist that must be completed in full. The purpose is to connect product names to the underlying problems they solve, identify the tools selected for hands-on learning, distinguish them from relevant alternatives, and show when each category belongs in the wider programme.

## Priority definitions

| Priority | Meaning |
|---|---|
| Core | Foundational capability that should be learned and practised directly. |
| Selected | The main product or framework chosen for hands-on implementation in this programme. |
| Adjacent | Important alternative or complementary technology that should be understood, but does not require equal implementation depth initially. |
| Later | Valuable after prerequisite concepts and tools are established. |
| Optional | Relevant to some roles or workloads, but not required for the central learning path. |

## Tool-selection principle

The programme does not aim to collect unrelated product names. Tools are introduced only after the corresponding problem is understood.

Examples:

- PostgreSQL follows relational modelling, keys, constraints, transactions, and SQL.
- Psycopg follows direct database connectivity and transaction control from Python.
- dbt follows SQL transformation and analytical modelling.
- Airflow or Azure Data Factory follows implementation of individual pipeline tasks.
- Docker follows a working application or pipeline.
- MLflow follows repeatable model training that produces parameters, metrics, and artifacts.
- Spark follows single-machine processing and the need for distributed computation.
- Kubernetes follows containers, deployment, health checks, and basic cloud operations.

## Core development and software foundations

| Capability | Main tool or technology | Priority | Planned phase | Role in practice |
|---|---|---:|---|---|
| Programming | Python | Core | All phases | Data processing, automation, APIs, testing, ML, pipelines, and services. |
| Querying and transformation | SQL | Core | Phases 1 onward | Retrieval, joins, aggregation, validation, warehouse transformation, and analytical modelling. |
| Version control | Git and GitHub | Core | All phases | Change history, collaboration, branching, pull requests, review, and CI/CD integration. |
| Development environment | VS Code | Selected | All phases | Primary workspace for Python, SQL, Markdown, configuration, testing, terminal use, and Git. |
| Command line | PowerShell, shell, and Linux foundations | Core | All phases | Local automation, server work, containers, cloud tooling, and CI environments. |
| Python environments | `venv` and `pip` | Core | Phase 3 onward | Isolated project dependencies and reproducible local development. |
| Python project metadata | `pyproject.toml` | Selected | Phase 3 onward | Dependency, packaging, testing, linting, and tool configuration. |
| Python testing | `pytest` | Selected | Phase 3 onward | Unit, integration, data-quality, and pipeline tests. |
| Python linting and formatting | Ruff | Selected | Phase 3 onward | Fast automated code-quality and formatting checks. |

## Relational databases and database access

| Capability | Main tool or technology | Priority | Planned phase | Role in practice |
|---|---|---:|---|---|
| Relational database | PostgreSQL | Selected | Phase 1 onward | Operational storage, transactions, constraints, SQL, views, indexes, and analytical source data. |
| Primary SQL workspace | PostgreSQL extension for VS Code | Selected | Phase 3 onward | Writing, saving, executing, and reviewing SQL inside the main project workspace. |
| Graphical administration | pgAdmin 4 | Adjacent | Phase 1 onward | Visual inspection of schemas, tables, constraints, roles, sessions, backups, and database objects. |
| Command-line database client | `psql` | Core | Phase 3 onward | Scripted, remote, container, and server-side PostgreSQL access. |
| Direct Python PostgreSQL driver | Psycopg 3 | Selected | Phase 3 | Explicit connections, cursors, parameterized SQL, transactions, commits, rollbacks, and error handling. |
| Database toolkit and abstraction | SQLAlchemy | Adjacent | Phase 3 or 6 | Connection management, SQL construction, transaction integration, and application-level database access. |
| Alternative desktop database client | DBeaver | Optional | As needed | Cross-database graphical client for environments where several database systems are used. |

## Data pipelines and orchestration

| Capability | Main tool or technology | Priority | Planned phase | Role in practice |
|---|---|---:|---|---|
| Local pipeline implementation | Python, SQL, Psycopg, and pandas | Selected | Phase 3 | Transparent extract, transform, validate, and load workflows. |
| Tabular processing | pandas | Selected | Phase 3 onward | Small-to-medium local transformations, validation, file ingestion, and analysis. |
| Workflow orchestration | Apache Airflow | Selected | Phase 5 | Task dependencies, schedules, retries, logs, backfills, and workflow state. |
| Managed Azure orchestration | Azure Data Factory | Selected later | Phases 5 and 8 | Managed ingestion, data movement, scheduling, and Azure-native workflow coordination. |
| Microsoft delivery platform | Azure DevOps and Azure Pipelines | Adjacent | Phases 6 and 8 | Repositories, work tracking, CI/CD, and enterprise Microsoft delivery workflows. |

## Warehouses, analytics engineering, and reporting

| Capability | Main tool or technology | Priority | Planned phase | Role in practice |
|---|---|---:|---|---|
| SQL transformation framework | dbt | Selected | Phase 4 | Modular SQL models, tests, documentation, lineage, and incremental transformations. |
| Cloud analytical warehouse | Snowflake | Adjacent | Phase 4 | Managed analytical storage and compute separation used in many modern data stacks. |
| Microsoft analytical platform | Microsoft Fabric | Adjacent | Phases 4 and 8 | Integrated data engineering, warehouse, lakehouse, analytics, and reporting workflows. |
| Microsoft analytical warehouse | Azure Synapse Analytics | Adjacent | Phase 8 | Azure-based SQL analytics, data integration, and warehouse workloads. |
| Business intelligence | Power BI | Adjacent | Phase 4 or later | Dashboards, semantic models, reporting, and delivery of analytical results to business users. |
| Columnar file format | Parquet | Core | Phase 4 | Efficient typed analytical storage and exchange. |
| Lakehouse table format | Delta Lake | Selected later | Phase 10 | Reliable tables, schema enforcement, versioning, and incremental processing on data lakes. |

## APIs, containers, delivery, and production applications

| Capability | Main tool or technology | Priority | Planned phase | Role in practice |
|---|---|---:|---|---|
| Python API framework | FastAPI | Selected | Phase 6 | Data services, model-serving endpoints, request validation, and online inference. |
| Containerization | Docker | Selected | Phase 6 | Reproducible runtime environments for pipelines, APIs, tests, and deployment. |
| Multi-container local environments | Docker Compose | Selected | Phase 6 | Coordinating PostgreSQL, applications, tracking services, and supporting components locally. |
| Continuous integration | GitHub Actions | Selected | Phase 6 | Automated formatting, testing, builds, and validation on repository changes. |
| Continuous delivery | GitHub Actions and selected Azure services | Selected later | Phases 6 and 8 | Automated packaging and deployment after successful checks. |

## MLOps and model lifecycle

| Capability | Main tool or technology | Priority | Planned phase | Role in practice |
|---|---|---:|---|---|
| Experiment tracking and model lifecycle | MLflow | Selected | Phase 7 | Parameters, metrics, artifacts, model packaging, registry concepts, and reproducibility. |
| Managed model development | Azure Machine Learning | Selected later | Phase 8 | Managed training, tracking, registries, endpoints, and cloud ML workflows. |
| Data and model monitoring | General monitoring patterns first | Core | Phases 7, 8, and 12 | Data quality, drift, service health, logs, metrics, alerts, and retraining signals. |

## Azure cloud platform

| Capability | Main Azure service or concept | Priority | Planned phase | Role in practice |
|---|---|---:|---|---|
| Cloud foundations | subscriptions, resource groups, regions, identities, and networking | Core | Phase 8 | Resource organization, security boundaries, deployment location, and access control. |
| Object and lake storage | Azure Storage and Azure Data Lake Storage | Selected | Phase 8 | Files, raw data, analytical data, and pipeline storage. |
| Managed relational storage | Azure Database for PostgreSQL or another justified option | Selected later | Phase 8 | Managed cloud relational database. |
| Secrets | Azure Key Vault | Selected | Phase 8 | Secure storage and controlled retrieval of credentials and secrets. |
| Container registry | Azure Container Registry | Selected | Phase 8 | Storage and distribution of container images. |
| Container deployment | Azure Container Apps or another justified service | Selected later | Phase 8 | Managed deployment of containerized jobs and services. |
| Monitoring | Azure Monitor and Log Analytics | Selected | Phase 8 | Centralized logs, metrics, alerting, and cloud diagnostics. |

## Distributed processing and data platforms

| Capability | Main tool or technology | Priority | Planned phase | Role in practice |
|---|---|---:|---|---|
| Distributed computation | Apache Spark | Selected | Phase 10 | Partitioned transformations, distributed joins, shuffles, caching, and large-scale processing. |
| Python interface to Spark | PySpark | Selected | Phase 10 | Spark processing using Python DataFrame and SQL APIs. |
| Managed data and AI platform | Databricks | Selected | Phase 10 | Spark, Delta Lake, workflows, notebooks, SQL, and MLflow integration. |

## Streaming and event systems

| Capability | Main tool or technology | Priority | Planned phase | Role in practice |
|---|---|---:|---|---|
| Event streaming | Apache Kafka | Selected | Phase 11 | Producers, consumers, topics, partitions, offsets, replay, and event-driven pipelines. |
| Stream processing | Spark Structured Streaming or another justified engine | Later | Phase 11 | Stateful and windowed processing of continuously arriving events. |

## Specialized data stores

| Workload | Representative tools | Priority | Planned phase | Role in practice |
|---|---|---:|---|---|
| Document storage | MongoDB and Azure Cosmos DB | Adjacent | Phase 9 | Flexible document models and nested semi-structured data. |
| Key-value and caching | Redis | Adjacent | Phase 9 | Low-latency lookup, caching, sessions, and transient state. |
| Graph traversal | Neo4j | Adjacent | Phase 9 | Relationship-heavy queries and path traversal. |
| Search | Elasticsearch or OpenSearch | Adjacent | Phase 9 | Full-text search, inverted indexes, and search-oriented retrieval. |
| Vector similarity | PostgreSQL with `pgvector` and dedicated vector systems | Adjacent | Phase 9 | Embedding storage and nearest-neighbour retrieval. |
| Time-series storage | PostgreSQL extensions or specialized time-series systems | Later | Phase 9 | Time-indexed measurements, retention, and time-oriented queries. |
| Wide-column storage | Cassandra-style systems | Later | Phase 9 | High-scale distributed writes and access-pattern-driven modelling. |

## Infrastructure, observability, and operations

| Capability | Main tool or technology | Priority | Planned phase | Role in practice |
|---|---|---:|---|---|
| Container orchestration | Kubernetes | Later | Phase 12 | Deployment, scaling, service discovery, rollouts, and recovery for containerized workloads. |
| Infrastructure as code | Terraform | Later | Phase 12 | Reproducible cloud infrastructure definitions and environment management. |
| Metrics and dashboards | Prometheus and Grafana | Adjacent | Phase 12 | Metrics collection, querying, dashboards, and alerts. |
| Logs and traces | Platform-native and open observability tooling | Later | Phases 8 and 12 | Diagnosis of application and infrastructure behavior. |

## GenAI application tooling

| Capability | Representative tools | Priority | Planned phase | Role in practice |
|---|---|---:|---|---|
| Model APIs and structured LLM integration | Direct provider SDKs and ordinary Python application code | Core when needed | After software foundations | Transparent, testable integration without unnecessary abstraction. |
| Retrieval-augmented generation | PostgreSQL with `pgvector`, search systems, or another justified retrieval layer | Adjacent | After database and API foundations | Retrieval, ranking, context construction, and evaluation. |
| GenAI orchestration frameworks | LangChain and LlamaIndex | Optional | After direct implementation | Convenience abstractions for selected workflows, evaluated against simpler direct implementations. |

## Learning depth policy

Not every tool receives the same depth.

The selected tools should eventually produce practical evidence. Adjacent tools should be understood well enough to compare architectures, read vacancy descriptions, and transfer concepts. Later tools are introduced only after their prerequisites. Optional tools are used only when a project requirement justifies them.

A vacancy may list several products that solve overlapping problems. The correct response is not to learn each interface independently. The programme should identify:

1. the underlying system problem;
2. the selected implementation used for deep practice;
3. the transferable concepts;
4. the main alternatives and their trade-offs;
5. the evidence required before claiming competence.

## Maintenance policy

This landscape should be revisited occasionally when:

- the intended role direction changes;
- repeated vacancy patterns reveal an important missing capability;
- a selected technology becomes unsuitable;
- a project requirement justifies an adjacent tool;
- the programme reaches a phase where a deferred selection must be made.

It does not require weekly updating. The master learning map remains the stable dependency-ordered programme, while this document provides a broader industry-facing map of tools and alternatives.