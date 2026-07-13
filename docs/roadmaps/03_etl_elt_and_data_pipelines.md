# Roadmap: ETL, ELT, and Data Pipelines

## Objective

Build reliable, repeatable, testable processes that move and transform data without requiring manual execution.

## Prerequisites

- SQL and relational databases
- basic Python
- data modelling foundations
- Git and environment management

## Part A: Pipeline concepts

1. sources, destinations, and interfaces
2. extraction, transformation, and loading
3. ETL versus ELT
4. batch versus streaming
5. jobs, steps, and dependencies
6. data lineage
7. control flow versus data flow

## Part B: Extraction

1. files
2. relational databases
3. APIs
4. authentication
5. pagination
6. rate limits
7. source consistency
8. change tracking
9. snapshots
10. schema discovery

## Part C: Loading patterns

1. append
2. overwrite
3. upsert
4. merge
5. full refresh
6. incremental load
7. checkpoints
8. watermarks
9. change data capture concepts

## Part D: Reliability

1. idempotency
2. retries
3. timeouts
4. partial failure
5. atomic publication
6. duplicate prevention
7. late-arriving records
8. backfills
9. reruns
10. recovery procedures

## Part E: Data quality

1. schema validation
2. type validation
3. completeness
4. uniqueness
5. ranges and domains
6. referential checks
7. freshness
8. volume anomalies
9. quarantine patterns
10. quality reporting

## Part F: Engineering structure

1. configuration
2. environment variables
3. secret handling
4. logging
5. exception handling
6. modular functions
7. command-line interfaces
8. unit tests
9. integration tests
10. local reproducibility

## Part G: Pipeline observability

1. run identifiers
2. start and end times
3. row counts
4. rejected rows
5. source checkpoints
6. logs
7. metrics
8. alerts
9. audit tables
10. operational dashboards

## Practical milestones

- ingest telecom CSV data into raw PostgreSQL tables
- validate and quarantine invalid rows
- implement safe incremental loading
- make repeated runs idempotent
- add structured logging and run metadata
- complete a historical backfill
- write unit and integration tests

## Completion criteria

- can explain ETL and ELT as architectural choices
- can implement safe incremental pipelines
- can recover from partial failures
- can validate and audit pipeline results
- can rerun and backfill without corrupting data
