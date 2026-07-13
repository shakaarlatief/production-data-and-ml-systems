# Roadmap: SQL and Relational Databases

## Objective

Develop a rigorous understanding of relational data and become able to design, query, validate, and maintain a PostgreSQL database independently.

The phase ends with a professionally documented telecom operational database and a correctly constructed customer-level analytical dataset.

## Learning standard

Every new SQL keyword, function, operator, symbol, and clause must be explained before it becomes assumed knowledge.

Each query should be studied using:

- input rows
- written syntax
- meaning of each component
- conceptual execution
- exact result
- row count
- row grain
- missing-value behavior
- common mistakes

## Part A: Relational foundations

### Lesson 1: Why databases exist

- limitations of disconnected files
- persistent shared data
- concurrent access
- consistency
- security
- transactions
- querying

### Lesson 2: Database terminology

- database
- database management system
- PostgreSQL
- server
- client
- connection
- database
- schema
- table
- row
- column
- data type

### Lesson 3: Entities, attributes, and grain

- entities
- attributes
- records
- one row represents what
- customer grain
- invoice grain
- customer-month grain
- why grain must be stated before joins and aggregation

### Lesson 4: Keys and relationships

- primary keys
- composite keys
- natural keys
- surrogate keys
- foreign keys
- referential integrity
- one-to-one
- one-to-many
- many-to-many
- bridge tables

### Lesson 4A: Relational and non-relational database models

This comparison is introduced early so that PostgreSQL is understood as a deliberate first choice rather than as the only possible database model.

- the relational model as the baseline
- non-relational as an umbrella category
- the meaning and limitations of the term NoSQL
- why non-relational does not mean that relationships are absent
- structured, semi-structured, and unstructured data
- document databases
- key-value databases
- wide-column databases
- graph databases
- search-oriented data stores
- time-series databases
- vector databases and vector search
- normalization versus denormalization and embedding
- joins versus nested documents and application-side composition
- strong consistency, eventual consistency, and replication as introductory concepts
- polyglot persistence
- workload-based technology selection
- why PostgreSQL remains the first hands-on database
- connection to `12_nosql_and_specialized_data_stores.md`

### Foundation milestone

Draw and explain a small model containing customers, contracts, invoices, and payments. State the grain and key of every table. Then explain at a high level how a document-oriented representation might differ and why the relational design remains appropriate for the first implementation.

## Part B: Reading one table

### Lesson 5: First SQL statement

Introduce each component separately:

```sql
SELECT *
FROM customers;
```

Topics:

- SQL statement
- `SELECT`
- `*` as all selected columns
- `FROM`
- table name
- semicolon
- result set

### Lesson 6: Selecting explicit columns

- one column
- several columns
- commas
- column order
- why `SELECT *` is often unsuitable in maintained code

### Lesson 7: Aliases

- `AS`
- column aliases
- table aliases
- temporary result naming
- difference between aliasing and renaming stored data

### Lesson 8: Literal values and expressions

- numeric literals
- text literals
- date literals
- arithmetic
- parentheses
- operator precedence
- calculated result columns
- `*` as multiplication versus `*` as all columns

### Lesson 9: Filtering with `WHERE`

Explain separately:

- equality
- inequality
- greater and less than
- `AND`
- `OR`
- `NOT`
- parentheses
- `IN`
- `BETWEEN`
- text pattern matching

### Lesson 10: Missing values

- meaning of `NULL`
- three-valued logic
- `IS NULL`
- `IS NOT NULL`
- why `= NULL` is not correct
- `COALESCE`
- missing versus zero
- missing versus empty text

### Lesson 11: Sorting and limiting

- `ORDER BY`
- ascending and descending
- multiple sort keys
- `LIMIT`
- deterministic ordering
- why storage order should not be assumed

### Lesson 12: Distinct results

- `DISTINCT`
- duplicate rows in a result
- difference between duplicate data and repeated values
- why `DISTINCT` should not hide an incorrect join

### Reading milestone

Answer a set of independent questions from one table without aggregation.

## Part C: Summarizing one table

### Lesson 13: Aggregate functions

Explain:

- function syntax
- input values
- output value
- `COUNT(*)`
- `COUNT(column)`
- `COUNT(DISTINCT column)`
- `SUM`
- `AVG`
- `MIN`
- `MAX`
- behavior with `NULL`

### Lesson 14: Grouping

- `GROUP BY`
- conceptual grouping
- one output row per group
- selected grouped columns
- aggregate expressions
- grain change

### Lesson 15: Filtering groups

- `HAVING`
- difference from `WHERE`
- logical query processing
- filtering before versus after aggregation

### Lesson 16: Conditional expressions

- `CASE`
- `WHEN`
- `THEN`
- `ELSE`
- `END`
- category creation
- binary indicators

### Lesson 17: Conditional aggregation

- counting rows that satisfy conditions
- summing flags
- category-specific totals
- avoiding repeated scans where appropriate

### Aggregation milestone

Build invoice, payment, and support summaries at customer grain.

## Part D: Combining tables

### Lesson 18: Manual row matching

Before SQL joins:

- identify keys
- state cardinality
- manually enumerate matches
- predict output row count
- state output grain

### Lesson 19: `INNER JOIN`

- left and right input
- `JOIN`
- `ON`
- equality condition
- qualified column names
- table aliases
- unmatched rows

### Lesson 20: `LEFT JOIN`

- preserving left rows
- missing matches
- generated `NULL` values
- counting after a left join
- `COUNT(*)` versus `COUNT(right_key)`

### Lesson 21: Other join forms

- `RIGHT JOIN`
- `FULL OUTER JOIN`
- `CROSS JOIN`
- self-join
- when each is useful

### Lesson 22: Cardinality and row multiplication

- one-to-one
- one-to-many
- many-to-one
- many-to-many
- accidental Cartesian multiplication
- duplicate keys
- pre-aggregation
- validation queries before and after joins

### Lesson 23: Safe multi-table feature construction

- aggregate each event table to target grain
- validate uniqueness
- join summaries
- verify row counts
- verify missingness
- preserve point-in-time boundaries

### Join milestone

Construct one row per customer from customers, contracts, invoices, payments, and support tickets without accidental multiplication.

## Part E: Structuring complex queries

### Lesson 24: Subqueries

- scalar subquery
- table subquery
- correlated subquery
- readability and performance considerations

### Lesson 25: Common table expressions

- `WITH`
- named intermediate results
- multi-stage transformations
- scope
- readability
- recursive CTE introduction

### Lesson 26: Set operations

- `UNION`
- `UNION ALL`
- `INTERSECT`
- `EXCEPT`
- column compatibility
- duplicate behavior

### Lesson 27: Window functions

Return formally to the previewed example:

```sql
COUNT(*) OVER (
    PARTITION BY customer_id
)
```

Explain:

- aggregate versus window calculation
- `OVER`
- partition
- preserving rows
- window ordering
- window frame

Functions:

- `COUNT`
- `SUM`
- `AVG`
- `ROW_NUMBER`
- `RANK`
- `DENSE_RANK`
- `LAG`
- `LEAD`
- running totals
- rolling calculations

### Advanced-query milestone

Produce customer histories, latest-record selections, running balances, and repeated group statistics while preserving required row grain.

## Part F: Creating and modifying data

### Lesson 28: PostgreSQL environment

- server
- service
- database
- user or role
- client
- connection parameters
- `psql`
- graphical client
- editor integration

### Lesson 29: Creating databases and schemas

- `CREATE DATABASE`
- `CREATE SCHEMA`
- naming
- ownership
- separation of concerns

### Lesson 30: Creating tables

- `CREATE TABLE`
- column definitions
- data types
- nullability
- defaults

### Lesson 31: Data types

- integer types
- exact numeric types
- floating-point types
- text
- Boolean
- dates
- timestamps
- time zones
- generated identifiers
- type selection trade-offs

### Lesson 32: Constraints

- `PRIMARY KEY`
- `FOREIGN KEY`
- `NOT NULL`
- `UNIQUE`
- `CHECK`
- `DEFAULT`
- constraint violations

### Lesson 33: Inserting data

- `INSERT`
- explicit column lists
- multiple rows
- returning inserted values

### Lesson 34: Updating and deleting

- `UPDATE`
- `SET`
- `DELETE`
- importance of `WHERE`
- preview changes before writes
- safe change workflow

### Lesson 35: Transactions

- `BEGIN`
- `COMMIT`
- `ROLLBACK`
- atomicity
- consistency
- isolation
- durability
- transaction boundaries
- failure scenarios

### Data-maintenance milestone

Create the telecom schema, load valid sample data, reject invalid data, and perform safe transactional updates.

## Part G: Database design

### Lesson 36: Functional dependencies

- determinants
- dependent attributes
- candidate keys
- why repeated facts cause anomalies

### Lesson 37: Normal forms

- first normal form
- second normal form
- third normal form
- practical interpretation
- limitations of purely mechanical normalization

### Lesson 38: Anomalies

- insertion anomaly
- update anomaly
- deletion anomaly

### Lesson 39: Many-to-many design

- junction tables
- composite uniqueness
- effective dates
- relationship attributes

### Lesson 40: Temporal data

- valid time
- transaction time
- current versus historical state
- effective dates
- overlapping intervals

### Design milestone

Design and justify a normalized operational schema for the telecom domain.

## Part H: Performance and maintainability

### Lesson 41: Indexes

- search structures
- index keys
- selectivity
- write overhead
- composite indexes
- order of index columns
- unnecessary indexes

### Lesson 42: Query plans

- planner
- estimated cost
- table scan
- index scan
- joins
- `EXPLAIN`
- `EXPLAIN ANALYZE`

### Lesson 43: Views and reusable queries

- views
- materialized views
- refresh
- permissions
- abstraction

### Lesson 44: Security foundations

- roles
- privileges
- ownership
- least privilege
- read-only access
- schema permissions

### Operations milestone

Diagnose selected slow queries, justify indexes, create reusable views, and establish basic access roles.

## Part I: Analytical dataset construction

### Lesson 45: Prediction definition

- target population
- observation unit
- prediction time
- outcome window
- feature window

### Lesson 46: Point-in-time features

- historical cutoffs
- latest known state
- event aggregation
- late-arriving data
- leakage prevention

### Lesson 47: Final customer feature table

Combine:

- customer attributes
- active contract state
- service subscriptions
- invoice history
- payment behavior
- support history
- usage summaries
- outcome definition

### Lesson 48: Validation

- one row per intended observation
- key uniqueness
- expected row count
- missingness
- impossible values
- temporal correctness
- reproducible build

## Phase completion criteria

The phase is complete when the learner can:

- explain relational concepts accurately
- distinguish relational databases from the major non-relational database families at an introductory level
- explain why PostgreSQL is the correct first implementation for this phase
- use PostgreSQL independently
- write and debug multi-table SQL
- predict join cardinality
- use aggregation and window functions appropriately
- create tables and constraints
- perform safe transactions
- design a normalized schema
- inspect query plans
- construct and validate a point-in-time analytical dataset
- document all decisions and limitations
