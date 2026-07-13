# Roadmap: Data Modelling and Analytical Dataset Construction

## Objective

Learn how to represent operational reality accurately and transform it into reliable analytical structures with explicit business meaning and historical correctness.

## Prerequisite

Completion of the relational foundations, joins, constraints, normalization, and analytical dataset sections of the SQL roadmap.

## Part A: Modelling foundations

1. business processes, entities, events, and states
2. conceptual, logical, and physical models
3. data grain as a design decision
4. natural and surrogate keys
5. relationship cardinality and optionality
6. data ownership and source-of-truth concepts
7. business definitions and naming conventions

## Part B: Operational modelling

1. normalized transaction-oriented schemas
2. current state versus event history
3. effective dating
4. audit columns
5. soft deletion
6. immutable events
7. master and reference data
8. schema evolution

## Part C: Analytical modelling

1. OLTP versus OLAP requirements
2. facts and dimensions
3. additive, semi-additive, and non-additive measures
4. transaction, periodic snapshot, and accumulating snapshot facts
5. conformed dimensions
6. star schemas
7. snowflake schemas
8. degenerate dimensions
9. role-playing dimensions
10. bridge tables

## Part D: Historical correctness

1. slowly changing dimensions
2. Type 1, Type 2, and selected alternatives
3. valid-time intervals
4. late-arriving facts and dimensions
5. restatements
6. point-in-time joins
7. reproducible historical reporting

## Part E: Metrics and semantic consistency

1. business metric definitions
2. numerator, denominator, filters, and grain
3. reusable measures
4. semantic layers
5. conflicting definitions
6. data contracts
7. ownership and approval

## Part F: Machine-learning datasets

1. prediction unit
2. observation time
3. feature windows
4. outcome windows
5. label construction
6. feature tables
7. point-in-time correctness
8. leakage
9. training-serving consistency
10. offline and online features

## Practical milestones

- design a normalized operational telecom model
- design a star schema for billing and support analysis
- implement historical contract tracking
- define a reusable customer metric layer
- build a point-in-time customer feature table
- document all grains, keys, and temporal assumptions

## Completion criteria

- can choose and justify operational and analytical models
- can state the grain of every table
- can preserve historical truth
- can define metrics without ambiguity
- can construct leakage-safe features
- can explain trade-offs between normalization and denormalization
