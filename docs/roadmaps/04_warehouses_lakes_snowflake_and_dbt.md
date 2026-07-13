# Roadmap: Warehouses, Lakes, Snowflake, and dbt

## Objective

Understand analytical storage architectures and manage SQL transformations as tested, documented, version-controlled software.

## Prerequisites

- strong SQL
- analytical data modelling
- batch pipeline foundations

## Part A: Analytical storage

1. operational versus analytical workloads
2. row-oriented versus column-oriented storage
3. scans, joins, and aggregations
4. data warehouses
5. separation of storage and compute
6. workload isolation
7. cost and performance trade-offs

## Part B: Data lakes

1. object storage
2. files and objects
3. CSV, JSON, Avro, and Parquet
4. schemas
5. partitioned datasets
6. small-file problems
7. raw, curated, and serving zones
8. metadata catalogs

## Part C: Lakehouse concepts

1. table metadata over object storage
2. transactions
3. schema enforcement
4. schema evolution
5. time travel
6. compaction
7. open table formats
8. warehouse and lake trade-offs

## Part D: Snowflake

1. account and database organization
2. databases, schemas, and tables
3. virtual warehouses
4. storage and compute separation
5. loading data
6. stages and file formats
7. roles and permissions
8. query history and cost
9. clustering concepts
10. semi-structured data
11. data sharing concepts

## Part E: dbt foundations

1. project structure
2. sources
3. models
4. `ref`
5. dependency graph
6. materializations
7. tests
8. documentation
9. lineage
10. seeds and snapshots

## Part F: dbt project design

1. staging models
2. intermediate models
3. marts
4. naming
5. reusable macros
6. generic and singular tests
7. model contracts
8. incremental models
9. snapshots
10. CI workflows

## Practical milestones

- store raw and curated files in a local object-storage-style layout
- compare CSV and Parquet behavior
- create a warehouse-style schema
- build a dbt project for telecom transformations
- add tests and documentation
- implement one incremental model
- reproduce selected models in Snowflake when access is available

## Completion criteria

- can distinguish warehouse, lake, and lakehouse architectures
- can justify file formats and partitioning
- can build maintainable dbt transformations
- can explain Snowflake's main architectural concepts
- can reason about performance and cost
