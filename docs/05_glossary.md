# Glossary

## Purpose

This glossary provides concise definitions and important distinctions. Detailed explanations belong in knowledge notes and roadmaps.

## Core data terms

### Database

An organized collection of data managed so that it can be stored, retrieved, changed, and protected systematically.

### Database management system

Software that manages databases. It handles storage, queries, permissions, transactions, constraints, and other database operations. PostgreSQL is a database management system.

### Relational database

A database that organizes data into relations, commonly represented as tables, and connects those tables through keys and constraints.

### Schema

A named organizational boundary inside a database that contains objects such as tables and views. The word can also refer more generally to the formal structure of data. Context determines the meaning.

### Table

A named relation containing rows and columns.

### Row

One record in a table. The meaning of one row is determined by the table's grain.

### Column

A named attribute recorded for every applicable row in a table.

### Data type

A rule describing what kind of value a column can store, such as integer, text, date, timestamp, or Boolean.

### Entity

A distinguishable real-world or conceptual object represented in data, such as a customer, invoice, contract, or support ticket.

### Grain

A precise statement of what one row represents. Examples include one row per customer, one row per invoice, or one row per customer per month.

### Primary key

A column or set of columns whose value uniquely identifies each row in a table.

### Foreign key

A column or set of columns that references a key in another table and represents a relationship between the tables.

### Referential integrity

The condition that references between tables remain valid. A foreign key should not refer to a parent row that does not exist, unless a permitted missing reference is explicitly allowed.

### Natural key

A key derived from an existing business identifier, such as an official customer number.

### Surrogate key

A generated identifier used internally, often because a business identifier is unstable, complex, or not unique across systems.

### Constraint

A database rule that restricts allowed data. Examples include primary keys, foreign keys, `NOT NULL`, `UNIQUE`, and `CHECK`.

### Transaction

A group of database operations treated as one logical unit. A successful transaction is committed; an unsuccessful one can be rolled back.

### Index

An additional data structure that can help the database locate rows efficiently, at the cost of storage and additional work during writes.

## SQL terms

### SQL

A language used to define, query, modify, and control data in relational database systems.

### Query

A request for data or an operation expressed in SQL.

### Statement

A complete SQL instruction, such as a `SELECT`, `CREATE TABLE`, or `UPDATE` statement.

### Expression

A combination of columns, values, operators, and functions that produces a value.

### Aggregate function

A function that summarizes multiple rows or values, such as `COUNT`, `SUM`, `AVG`, `MIN`, or `MAX`.

### Grouping

Dividing rows into sets that share specified values so that aggregate calculations can be performed per set.

### Join

An operation that combines rows from two data sources according to a matching condition.

### Window function

A calculation across a related set of rows that preserves the original result rows instead of collapsing them into one row per group.

### `NULL`

SQL's marker for a missing or unknown value. It is not the same as zero, an empty string, or the text `"NULL"`.

### View

A named query that can be used like a table. A standard view stores the query definition rather than a separate copy of its result.

## Data architecture terms

### Operational database

A database designed primarily to support day-to-day application transactions and current operational state.

### OLTP

Online transaction processing. Workloads with frequent small reads and writes, such as creating orders, recording payments, or updating accounts.

### Analytical database

A database optimized for analysis across large datasets, often involving scans, aggregations, and historical comparisons.

### OLAP

Online analytical processing. Workloads centered on reporting, aggregation, multidimensional analysis, and historical data.

### Data warehouse

A centralized analytical data platform containing integrated, structured, and historically useful data for reporting and analysis.

### Data lake

A storage environment that holds large amounts of raw or processed data in files or objects, including structured, semi-structured, and unstructured forms.

### Lakehouse

An architecture that combines data-lake storage with table management, reliability, and analytical capabilities associated with warehouses.

### Fact table

An analytical table containing measurable events or observations at a declared grain, such as one row per invoice line or service usage event.

### Dimension table

An analytical table containing descriptive context used to analyze facts, such as customers, products, dates, or regions.

### Star schema

An analytical model in which a central fact table connects to surrounding dimension tables.

### Slowly changing dimension

A strategy for handling changes to descriptive attributes over time while preserving an appropriate form of history.

### Feature table

A table containing model inputs at a clearly defined entity, time, and prediction grain.

### Point-in-time correctness

The requirement that each training or prediction row uses only information that would have been available at its specified reference time.

### Target leakage

The inclusion of information in model inputs that would not legitimately be available when the prediction is made, especially information caused by or recorded after the target outcome.

## Pipeline terms

### Data pipeline

An automated sequence that moves or transforms data from one or more sources to one or more destinations.

### ETL

Extract, transform, load. Data is transformed before it is loaded into the main destination.

### ELT

Extract, load, transform. Raw or lightly processed data is loaded first, then transformed using the destination platform.

### Batch processing

Processing a bounded collection of data at scheduled or triggered intervals.

### Streaming

Processing a continuing sequence of events as they arrive or in small ongoing windows.

### Full refresh

Rebuilding a complete target dataset from all relevant source data.

### Incremental load

Processing only new or changed data since a known checkpoint.

### Idempotency

The property that repeating an operation with the same inputs does not create unintended additional effects.

### Watermark

A recorded boundary, often a timestamp or identifier, used to determine which source records have already been processed.

### Backfill

Running a pipeline for historical periods or data that was missed previously.

### Data validation

Checking whether data satisfies expected rules concerning schema, ranges, uniqueness, completeness, relationships, or other properties.

### Orchestration

Coordinating when tasks run, in what order, with which dependencies, retries, schedules, and operational controls.

### DAG

Directed acyclic graph. A graph of tasks and dependencies with no path that loops back to an earlier task.

## Software and deployment terms

### API

An interface through which one software system can request functionality or data from another.

### REST

A common style for web APIs using resources, HTTP methods, and structured request and response messages.

### Endpoint

A specific address and operation exposed by an API or managed service.

### Batch inference

Generating predictions for a collection of observations in a scheduled or triggered job.

### Online inference

Generating a prediction in response to an individual request, usually with a latency requirement.

### Docker image

An immutable package containing an application, dependencies, and runtime instructions.

### Docker container

A running instance created from a Docker image.

### Container registry

A service that stores and distributes container images.

### CI

Continuous integration. Automated validation of code changes, commonly through tests, linting, and build checks.

### CD

Continuous delivery or continuous deployment. Automated preparation or release of validated software changes.

## MLOps terms

### MLOps

Practices and systems for developing, tracking, validating, deploying, monitoring, and maintaining machine-learning models reliably.

### Experiment tracking

Recording training runs, parameters, metrics, code references, artifacts, and related metadata.

### Model artifact

A serialized trained model and any associated files needed to use or inspect it.

### Model registry

A system for managing model versions, metadata, lineage, stages, approvals, and deployment status.

### Data drift

A change in the statistical distribution of model inputs.

### Prediction drift

A change in the distribution of model outputs.

### Concept drift

A change in the relationship between model inputs and the target outcome.

### Retraining

Fitting a new model version using updated data, code, configuration, or methodology.

### Rollback

Returning a deployed system to a previously known working version.

## Cloud and infrastructure terms

### Cloud computing

On-demand access to managed computing, storage, networking, databases, and application services operated by a provider.

### Virtual machine

A software-defined computer with its own operating system running on shared physical infrastructure.

### Managed service

A service for which the provider operates substantial parts of the underlying infrastructure, maintenance, scaling, backups, or availability.

### Identity and access management

Systems and policies that determine which identities may perform which actions on which resources.

### Secret

Sensitive configuration such as a password, access token, API key, or certificate.

### Observability

The ability to understand a system's internal state using outputs such as logs, metrics, and traces.

### Log

A timestamped record of an event produced by a system or application.

### Metric

A numerical measurement tracked over time, such as error rate, latency, throughput, or resource use.

### Trace

A record that follows one request or operation across multiple components.

### Infrastructure as code

Defining and managing infrastructure through version-controlled configuration rather than manual interface actions.

### Kubernetes

A system for deploying, scaling, and managing containerized applications.

### Terraform

A tool for declaring and managing infrastructure through configuration files and provider APIs.

## Distributed and streaming terms

### Distributed processing

Dividing data and computation across multiple machines that coordinate to complete a workload.

### Partition

A subset of data used as a unit of storage or parallel processing. The exact meaning depends on the system.

### Shuffle

Redistribution of data between workers, commonly required for distributed joins, grouping, or aggregation.

### Event

A record that something occurred at a particular time, such as a payment, page view, or contract change.

### Producer

An application that writes events to a streaming platform.

### Consumer

An application that reads and processes events from a streaming platform.

### Topic

A named stream or category of events in Kafka.

### Offset

A position identifying an event within a Kafka partition.

### Consumer group

A set of consumers that coordinate to divide the partitions of a topic among themselves.
