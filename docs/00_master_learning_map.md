# Master Learning Map

## Purpose

This document defines the complete learning programme for production data and machine-learning systems. It is the stable high-level map for the repository. Detailed lesson order, exercises, and implementation requirements belong in the topic roadmaps.

The programme begins with relational data and SQL, then moves through data modelling, pipelines, storage platforms, orchestration, software delivery, MLOps, cloud services, distributed processing, streaming, and production infrastructure. The ordering is intentional. Later subjects depend on concepts established earlier.

## Guiding principle

A technology should be introduced only after the underlying problem is understood.

Examples:

- PostgreSQL is introduced after tables, keys, relationships, and SQL are understood.
- dbt is introduced after SQL transformations and analytical modelling are understood.
- Airflow is introduced after individual pipeline tasks can be implemented.
- Docker is introduced after a working application exists.
- MLflow is introduced after model training produces parameters, metrics, and artifacts that need systematic tracking.
- Azure is introduced after local versions of storage, databases, pipelines, training, deployment, and monitoring are understood.
- Spark is introduced after single-machine tabular processing is understood.
- Kubernetes is introduced after containers and deployment are understood.

## End-to-end destination

The final system should demonstrate the following lifecycle:

```text
Operational source systems
        |
        v
Data ingestion
        |
        v
Raw storage
        |
        v
Validated and transformed data
        |
        v
Analytical warehouse models
        |
        v
Machine-learning feature tables
        |
        v
Tracked model training and evaluation
        |
        v
Model registry
        |
        v
Batch and online inference
        |
        v
Monitoring, alerting, and retraining
```

## Phase 1: SQL and relational databases

### Central question

How do organizations store structured operational data, preserve relationships and integrity, and retrieve the exact data needed for analysis?

### Main subjects

- databases and database management systems
- schemas, tables, rows, columns, and data types
- primary keys, foreign keys, and relationships
- SQL query structure
- filtering, sorting, expressions, and missing values
- aggregation and grouping
- joins and join cardinality
- subqueries and common table expressions
- window functions
- creating and modifying tables
- constraints and referential integrity
- transactions
- indexes and query plans
- normalization
- PostgreSQL
- constructing a customer-level analytical dataset

### Practical result

A local PostgreSQL database containing realistic telecom-style operational tables, together with documented SQL queries and exercises.

### Completion evidence

- can explain relational concepts without relying on memorized syntax
- can write correct multi-table SQL independently
- can identify and prevent join multiplication
- can design normalized operational tables
- can construct a leakage-safe modelling table at a defined grain and prediction time

## Phase 2: Data modelling and analytical dataset construction

### Central question

How should data be organized so that operational systems remain reliable and analytical users receive consistent, historically correct datasets?

### Main subjects

- operational versus analytical data models
- entity relationships and data grain
- normalization and denormalization
- fact and dimension tables
- star and snowflake schemas
- surrogate and natural keys
- slowly changing dimensions
- event time, processing time, and snapshot time
- data contracts and business definitions
- feature tables and point-in-time correctness
- target leakage
- semantic layers and reusable metrics

### Practical result

An analytical model that converts normalized telecom operations into reusable customer, billing, support, and usage datasets.

## Phase 3: ETL, ELT, and data pipelines

### Central question

How does data move reliably from source systems into analytical storage without manual execution?

### Main subjects

- extraction, transformation, and loading
- ETL versus ELT
- batch pipelines
- full refresh versus incremental loading
- idempotency
- checkpoints and watermarks
- retries and failure handling
- logging and observability
- configuration and secrets
- data validation
- schema evolution
- backfills
- pipeline testing
- Python and SQL pipeline implementation

### Practical result

A repeatable local ingestion and transformation pipeline that can be rerun safely and produces auditable outputs.

## Phase 4: Warehouses, lakes, lakehouses, Snowflake, and dbt

### Central question

Where should analytical data live, and how should transformations be managed as a version-controlled software project?

### Main subjects

- operational databases versus analytical warehouses
- row-oriented versus column-oriented storage
- data warehouses
- object storage and data lakes
- file formats such as CSV, JSON, and Parquet
- partitioning
- lakehouse concepts
- Snowflake architecture and SQL workflows
- dbt models, sources, tests, documentation, and lineage
- staging, intermediate, and mart layers
- incremental models
- data quality and contracts

### Practical result

A warehouse-style analytical layer with modular transformations, tests, documentation, and lineage.

## Phase 5: Workflow orchestration

### Central question

How are multiple tasks scheduled, ordered, retried, monitored, and backfilled as one dependable workflow?

### Main subjects

- jobs, tasks, dependencies, and directed acyclic graphs
- scheduling
- orchestration versus processing
- Airflow
- Azure Data Factory
- task retries and timeouts
- sensors and external dependencies
- parameterized workflows
- backfills
- operational metadata
- alerting
- local development and deployment patterns

### Practical result

An orchestrated workflow that ingests data, validates it, runs transformations, builds features, trains a model, and records the result.

## Phase 6: APIs, software engineering, Docker, and CI/CD

### Central question

How does working Python code become a testable, reproducible, deployable service?

### Main subjects

- package structure
- configuration management
- logging
- error handling
- unit, integration, and end-to-end tests
- REST concepts
- FastAPI
- request and response validation
- batch jobs versus online services
- Docker images and containers
- Docker Compose
- environment variables and secrets
- continuous integration
- continuous delivery
- GitHub Actions
- artifact building and release discipline

### Practical result

A tested batch application and prediction API packaged in Docker, with automated checks in CI.

## Phase 7: MLOps and MLflow

### Central question

How are model experiments, versions, approvals, deployments, monitoring, and retraining managed systematically?

### Main subjects

- reproducible training
- experiment tracking
- parameters, metrics, tags, and artifacts
- data and code lineage
- MLflow Tracking
- model packaging
- model registries
- promotion and rollback
- batch inference
- online inference
- model validation gates
- model and data monitoring
- data drift, prediction drift, and concept drift
- retraining triggers
- champion and challenger patterns
- auditability and governance

### Practical result

A tracked training workflow with registered model versions, reproducible artifacts, deployment gates, and monitoring specifications.

## Phase 8: Azure and cloud infrastructure

### Central question

How are the preceding local concepts implemented using managed cloud services?

### Main subjects

- cloud service models
- subscriptions, resource groups, regions, and resource naming
- identity and access management
- Azure Storage and Data Lake Storage
- managed relational databases
- Azure Data Factory
- Azure Machine Learning
- Azure Container Registry
- Azure Container Apps and related deployment options
- Azure Key Vault
- Azure Monitor and Log Analytics
- networking foundations
- cost management
- infrastructure configuration
- cloud security and least privilege

### Practical result

A cloud version of the local system with managed storage, pipelines, model training, deployment, secrets, and monitoring.

## Phase 9: Spark and Databricks

### Central question

What changes when data or computation no longer fits comfortably on one machine?

### Main subjects

- distributed systems foundations
- partitions
- lazy evaluation
- transformations and actions
- Spark DataFrames and Spark SQL
- PySpark
- shuffles
- joins and aggregations at scale
- caching and persistence
- partitioning and file layout
- execution plans
- structured streaming introduction
- Databricks workspaces and jobs
- Delta Lake and table reliability

### Practical result

A distributed transformation workflow that produces the same logical analytical outputs as the local pipeline while exposing the trade-offs of distributed execution.

## Phase 10: Kafka and streaming systems

### Central question

How are continuously arriving events transported, processed, stored, and consumed reliably?

### Main subjects

- events and streams
- producers and consumers
- topics, partitions, offsets, and consumer groups
- delivery semantics
- ordering
- event schemas
- replay
- retention
- stream processing
- windowing
- late-arriving events
- Kafka
- integration with storage and analytics
- real-time features and predictions

### Practical result

A small event-driven pipeline that publishes telecom events, consumes them, validates them, and writes them to an analytical destination.

## Phase 11: Production infrastructure

### Central question

How are production services provisioned, secured, scaled, observed, and recovered?

### Main subjects

- Kubernetes concepts
- pods, deployments, services, and ingress
- container orchestration
- Terraform and infrastructure as code
- environments and state
- identity, secrets, and network controls
- observability
- metrics, logs, and traces
- service-level indicators and objectives
- scaling
- reliability and failure recovery
- cost control
- backup and disaster recovery
- production runbooks

### Practical result

A documented and reproducible deployment architecture with infrastructure definitions, monitoring, and operational procedures.

## Phase 12: Integrated end-to-end project

The final phase combines the preceding work into one portfolio-ready system.

### Required characteristics

- realistic source data and operational tables
- automated ingestion
- validated raw and transformed layers
- analytical models and feature tables
- scheduled workflows
- tracked model training
- registered model artifacts
- batch and online predictions
- containerized services
- cloud deployment
- monitoring and alerting
- reproducible infrastructure
- detailed technical documentation
- explicit design decisions and limitations

## Cross-cutting competencies

The following skills are developed throughout all phases:

- Git and version control
- Linux and command-line foundations
- Python software engineering
- testing
- configuration management
- security and secret handling
- data quality
- observability
- reproducibility
- cost awareness
- documentation
- architecture reasoning
- communication of trade-offs

## Review policy

A phase is not complete merely because its material has been read. Completion requires explanation, guided practice, independent practice, application, and later review. The competency register defines these statuses in detail.
