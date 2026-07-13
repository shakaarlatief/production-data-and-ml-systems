# Roadmap: Workflow Orchestration

## Objective

Coordinate multiple data and ML tasks with explicit dependencies, schedules, retries, backfills, and operational visibility.

## Prerequisites

- working pipeline tasks
- logging and configuration
- SQL and Python
- basic testing

## Part A: Orchestration foundations

1. task
2. job
3. workflow
4. dependency
5. directed acyclic graph
6. scheduler
7. worker
8. executor
9. state
10. metadata database

## Part B: Workflow behavior

1. schedules
2. event triggers
3. retries
4. retry delay
5. timeout
6. failure propagation
7. conditional tasks
8. parameters
9. concurrency
10. resource limits

## Part C: Airflow

1. DAG definitions
2. operators
3. tasks
4. task instances
5. scheduling semantics
6. catchup
7. backfills
8. sensors
9. connections and variables
10. local deployment
11. logs and user interface
12. testing DAGs

## Part D: Azure Data Factory

1. pipelines
2. activities
3. datasets
4. linked services
5. integration runtimes
6. triggers
7. parameters
8. monitoring
9. data movement
10. calling external compute

## Part E: Production concerns

1. idempotent tasks
2. atomic outputs
3. rerun boundaries
4. data intervals
5. late data
6. external dependencies
7. alerting
8. service-level expectations
9. operational runbooks
10. deployment and versioning

## Practical milestones

- orchestrate ingestion and transformation tasks
- add retries and failure simulation
- run a historical backfill
- parameterize a date-based workflow
- trigger model training only after feature completion
- compare Airflow and Azure Data Factory responsibilities

## Completion criteria

- can distinguish orchestration from processing
- can design reliable DAGs
- can reason about schedules and data intervals
- can recover and backfill safely
- can monitor and diagnose failed workflows
