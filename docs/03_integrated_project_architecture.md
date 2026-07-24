# Integrated Project Architecture

## Purpose

This document describes the system that will be built gradually as the learning programme progresses. The architecture is intentionally evolutionary. Each phase adds a capability only after its foundations are understood.

## Project theme

The project represents a simplified telecommunications organization. It will contain operational data such as:

- customers
- contracts
- service subscriptions
- invoices
- payments
- support tickets
- usage events
- cancellations
- marketing interactions

The theme provides continuity across SQL, data engineering, cloud, and MLOps without reusing the existing Telco Customer Churn modelling repository.

## Relationship to focused learning implementations

Individual phases may use smaller external datasets when they provide a clearer and more realistic way to learn a particular capability.

The initial ETL implementation uses official Citi Bike trip-history data to develop file ingestion, source profiling, validation, staging, transactional loading, reconciliation, logging, testing, and rerun safety. This focused case study does not replace the telecommunications theme of the long-term integrated system.

The distinction is:

```text
Citi Bike ETL case study
    -> focused implementation for the current ETL phase

Telecommunications system
    -> long-term integrated architecture across all phases
```

Reusable design patterns, code structure, tests, operational practices, and lessons from the Citi Bike implementation may later be transferred into the integrated telecommunications system.

## Architectural principle

The system begins locally and grows toward managed cloud infrastructure.

This separates two questions:

1. What does the component do?
2. How does a cloud platform provide or manage that component?

Understanding the first question makes the second substantially easier.

## Stage 1: Local relational system

```text
Small source files or generated events
                |
                v
          PostgreSQL
                |
                v
      SQL queries and views
                |
                v
 Customer-level analytical dataset
```

### Learning goals

- understand relational storage
- create normalized tables
- enforce keys and constraints
- retrieve and combine data with SQL
- define and preserve row grain
- build an analytical dataset

## Stage 2: Local ingestion and transformation

```text
Source files and source tables
                |
                v
       Python ingestion jobs
                |
                v
         Raw database schema
                |
                v
    Validated transformation layer
                |
                v
       Analytical data models
```

### New capabilities

- repeatable ingestion
- configuration
- logging
- validation
- incremental loading
- safe reruns
- failure handling

## Stage 3: Warehouse-style modelling

```text
Raw layer
   |
   v
Staging models
   |
   v
Intermediate models
   |
   v
Fact and dimension models
   |
   v
Analytical marts and feature tables
```

### New capabilities

- explicit modelling layers
- dbt transformations
- tests
- lineage
- documentation
- reusable business definitions

## Stage 4: Orchestrated workflows

```text
Schedule or event
        |
        v
     Orchestrator
        |
        +--> ingest source data
        +--> validate raw data
        +--> run transformations
        +--> build feature table
        +--> train model
        +--> record artifacts
```

### New capabilities

- task dependencies
- retries
- backfills
- operational status
- alerts
- parameterized runs

## Stage 5: Model lifecycle

```text
Feature table
     |
     v
Tracked training run
     |
     v
Evaluation and validation
     |
     v
Model registry
     |
     +--> batch scoring
     |
     +--> online prediction API
```

### New capabilities

- experiment tracking
- reproducible training
- model packaging
- versioned models
- promotion and rollback
- batch and online inference

## Stage 6: Containerized delivery

```text
Application source
       |
       v
   Docker image
       |
       v
Container registry
       |
       v
Batch worker or API service
```

### New capabilities

- reproducible runtime environments
- automated tests
- image building
- deployment automation
- health checks

## Stage 7: Azure implementation

A later cloud version may use services that correspond to the local concepts:

| Local capability | Azure-oriented implementation |
|---|---|
| Files and object storage | Azure Blob Storage or Azure Data Lake Storage |
| PostgreSQL database | Azure Database for PostgreSQL |
| Pipeline coordination | Azure Data Factory or another selected orchestrator |
| Model training and registry | Azure Machine Learning |
| Container images | Azure Container Registry |
| Container deployment | Azure Container Apps or another justified target |
| Secrets | Azure Key Vault |
| Logs and metrics | Azure Monitor and Log Analytics |

The exact cloud architecture remains a design decision to be made after the local implementations expose concrete requirements.

## Stage 8: Distributed and streaming extensions

Distributed processing and streaming are added only when the project includes workloads that justify them.

```text
High-volume historical data ----> Spark or Databricks ----> analytical tables

Continuous application events --> Kafka ---------------> stream consumers
                                                        |
                                                        v
                                                storage and features
```

## Target end-state

```text
Operational applications and event producers
                    |
                    v
          Batch and streaming ingestion
                    |
                    v
             Raw storage layer
                    |
                    v
       Validated transformation layers
                    |
                    v
        Warehouse and feature models
                    |
                    v
     Orchestrated model training pipeline
                    |
                    v
       Experiment tracking and registry
                    |
             +------+------+
             |             |
             v             v
        Batch scoring   Online API
             |             |
             +------+------+
                    |
                    v
       Monitoring, alerts, and retraining
```

## Non-functional requirements

The final architecture should address:

- reproducibility
- testability
- data quality
- idempotency
- security
- least-privilege access
- secret management
- observability
- failure recovery
- scalability
- cost awareness
- auditability
- documentation

## Current architecture status

The long-term telecommunications architecture remains conceptual. A focused local implementation has begun through the Citi Bike ETL case study, which is currently providing the first concrete evidence for Stage 2 capabilities such as source acquisition, Python-to-PostgreSQL connectivity, source profiling, validation design, and layered storage.
