# Roadmap: Spark and Databricks

## Objective

Understand distributed data processing and use Spark effectively when workload scale or architecture justifies it.

## Prerequisites

- strong SQL
- pandas or equivalent tabular processing
- data pipelines
- warehouses and file formats
- basic cloud storage concepts

## Part A: Distributed foundations

1. cluster
2. driver
3. worker
4. executor
5. partition
6. parallelism
7. network cost
8. fault tolerance
9. data locality
10. distributed trade-offs

## Part B: Spark programming model

1. Spark session
2. DataFrame
3. schema
4. transformations
5. actions
6. lazy evaluation
7. lineage
8. stages
9. tasks
10. jobs

## Part C: Data operations

1. reading files and tables
2. selecting and filtering
3. expressions
4. grouping
5. joins
6. window functions
7. user-defined functions and their trade-offs
8. Spark SQL
9. writing outputs
10. partitioned data

## Part D: Performance

1. narrow and wide transformations
2. shuffle
3. join strategies
4. broadcast joins
5. partition sizing
6. skew
7. caching
8. predicate pushdown
9. column pruning
10. execution plans

## Part E: Databricks and Delta

1. workspace
2. notebooks and repositories
3. clusters and serverless compute concepts
4. jobs
5. data access
6. Delta tables
7. transactions
8. schema enforcement
9. time travel
10. optimization and maintenance

## Part F: Structured streaming introduction

1. unbounded tables
2. sources and sinks
3. triggers
4. checkpoints
5. event time
6. watermarks
7. windows
8. late data

## Practical milestones

- reproduce selected SQL transformations in PySpark
- inspect logical and physical plans
- demonstrate a shuffle
- diagnose skew or inefficient partitioning
- write partitioned Parquet or Delta data
- run a Databricks job
- implement a small structured-streaming example

## Completion criteria

- can explain why distributed execution is different
- can identify expensive shuffles
- can choose between pandas, SQL, and Spark appropriately
- can optimize common Spark transformations
- can use Delta-style table guarantees
