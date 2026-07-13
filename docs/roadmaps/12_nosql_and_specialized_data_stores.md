# Roadmap: NoSQL and Specialized Data Stores

## Objective

Understand the major non-relational and specialized storage models, the workload characteristics that motivate them, and the trade-offs involved in choosing one system rather than another.

The objective is not to replace relational databases or to collect product names. The objective is to learn how different data models, access patterns, consistency requirements, scale requirements, and operational constraints lead to different storage decisions.

## Recommended study point

This roadmap should be studied after the foundations of:

- relational databases and SQL
- data modelling
- ETL, ELT, and pipelines
- analytical storage architectures

It should be completed before or alongside the more advanced distributed-processing and streaming phases.

## Learning standard

For every storage model, study:

- the problem it is designed to solve
- its logical data model
- how data is identified and retrieved
- how relationships are represented
- how writes and updates work
- indexing
- transactions and consistency
- partitioning and replication
- failure behavior
- scaling behavior
- operational complexity
- suitable and unsuitable workloads
- comparison with PostgreSQL

## Part A: Relational and non-relational foundations

### Lesson 1: What non-relational means

- relational model as a baseline
- non-relational as an umbrella category
- NoSQL as a historical and practical label
- why NoSQL does not necessarily mean that SQL is impossible
- why non-relational does not mean that relationships do not exist
- structured, semi-structured, and unstructured data
- schema-on-write and schema-on-read
- flexible schema versus absent schema

### Lesson 2: Workload-first database selection

- read and write patterns
- point lookups
- range scans
- joins
- aggregations
- relationship traversal
- full-text search
- time-ordered ingestion
- vector similarity search
- latency
- throughput
- durability
- availability
- consistency
- geographic distribution
- operational cost

### Lesson 3: Modelling trade-offs

- normalization
- denormalization
- embedding
- duplication
- precomputed views
- application-side joins
- database-side joins
- update fan-out
- stale copies
- source of truth

### Foundation milestone

Given several workloads, explain why a relational database, document database, key-value store, graph database, or another specialized system would be a reasonable or unreasonable choice.

## Part B: Document databases

### Lesson 4: Document model

- documents
- fields
- nested objects
- arrays
- collections
- document identifiers
- JSON-like structures
- heterogeneous documents
- validation rules

### Lesson 5: Embedding versus referencing

- keeping related data inside one document
- referencing another document
- one-to-one, one-to-many, and many-to-many modelling
- document growth
- duplication
- update frequency
- bounded and unbounded arrays
- atomic update boundaries

### Lesson 6: Querying and indexing documents

- field queries
- nested-field queries
- array queries
- projections
- compound indexes
- multikey indexes
- aggregation pipelines
- index selectivity

### Lesson 7: Transactions and consistency

- single-document atomicity
- multi-document transactions
- read concerns and write concerns as concepts
- replication
- failover
- eventual consistency scenarios

### Representative technology

MongoDB or an equivalent document database.

### Practical milestone

Model customer profiles, contact preferences, and a bounded set of service attributes as documents. Compare the design with normalized PostgreSQL tables and document the consequences of embedding and referencing.

## Part C: Key-value stores and caches

### Lesson 8: Key-value model

- key
- value
- namespace
- exact-key lookup
- opaque versus structured values
- expiration
- in-memory storage
- persistence options

### Lesson 9: Common key-value use cases

- caching
- sessions
- counters
- rate limiting
- distributed locks
- queues and streams
- temporary state
- feature retrieval

### Lesson 10: Cache design

- cache-aside
- read-through and write-through concepts
- time to live
- eviction
- cache invalidation
- stale data
- cache stampede
- key naming
- serialization

### Representative technology

Redis or an equivalent key-value and in-memory data store.

### Practical milestone

Add a cache for frequently requested customer or prediction information. Measure the behavior with cache hits, misses, expiration, and invalidation.

## Part D: Wide-column databases

### Lesson 11: Wide-column model

- partition key
- clustering key
- rows and column families
- sparse columns
- denormalized query-oriented tables
- access-pattern-first modelling

### Lesson 12: Distributed write architecture

- horizontal partitioning
- replication
- leaderless concepts
- tunable consistency
- quorum concepts
- high write throughput
- failure tolerance

### Lesson 13: Query limitations and modelling consequences

- limited joins
- limited ad hoc queries
- one table per access pattern
- duplicated data
- partition size
- hot partitions
- time-series-like event storage

### Representative technology

Apache Cassandra or an equivalent wide-column database.

### Practical milestone

Design a high-volume telecom usage-event model around explicit access patterns. The implementation may remain conceptual until the distributed-systems foundations are ready.

## Part E: Graph databases

### Lesson 14: Property graph model

- nodes
- relationships
- labels
- relationship types
- properties
- paths
- direction

### Lesson 15: Graph-oriented questions

- neighborhood queries
- shortest paths
- connected components
- recommendation relationships
- fraud networks
- dependency graphs
- knowledge graphs

### Lesson 16: Graph modelling

- entity nodes
- event nodes
- relationship properties
- dense nodes
- traversal depth
- graph indexes
- avoiding relational-table thinking inside a graph model

### Representative technology

Neo4j or an equivalent property graph database.

### Practical milestone

Represent customers, devices, addresses, payment instruments, and support interactions as a graph. Use traversals to identify shared relationships that are awkward to express through repeated relational joins.

## Part F: Search-oriented data stores

### Lesson 17: Search engine data model

- documents
- inverted indexes
- tokens
- analyzers
- stemming
- stop words
- exact fields versus analyzed text
- relevance scores

### Lesson 18: Search workloads

- full-text search
- filtering
- faceting
- autocomplete
- log search
- near-real-time indexing
- search relevance

### Lesson 19: Search as a secondary system

- primary source of truth
- indexing pipeline
- synchronization
- reindexing
- stale search results
- schema mappings

### Representative technology

Elasticsearch, OpenSearch, or an equivalent search engine.

### Practical milestone

Build a searchable support-ticket index and compare full-text search with relational `LIKE` or text-search capabilities.

## Part G: Time-series databases

### Lesson 20: Time-series workload

- timestamped measurements
- append-heavy ingestion
- tags and fields
- high-cardinality dimensions
- retention
- downsampling
- rolling aggregations

### Lesson 21: Time-series storage design

- time partitioning
- compression
- retention policies
- continuous aggregates
- late-arriving measurements
- out-of-order data

### Representative technologies

A dedicated time-series database or a relational extension such as TimescaleDB.

### Practical milestone

Store service-performance or network measurements and produce time-windowed summaries with retention and downsampling rules.

## Part H: Vector databases and vector search

### Lesson 22: Vector representations

- vector
- dimension
- embedding
- similarity
- distance metrics
- cosine similarity
- Euclidean distance
- dot product

### Lesson 23: Approximate nearest-neighbor search

- exact versus approximate search
- index structures as concepts
- recall and latency trade-offs
- metadata filters
- update behavior
- memory and storage cost

### Lesson 24: Vector database boundaries

- vector database versus vector index
- vector extensions inside relational databases
- source text and metadata storage
- retrieval-augmented generation
- evaluation
- freshness
- deletion and governance

### Representative technologies

A vector-capable relational database, search engine, or dedicated vector system. The technology should be chosen from the project requirements rather than selected merely because it is marketed as a vector database.

### Practical milestone

Create embeddings for support-ticket text, retrieve similar historical cases, and compare a PostgreSQL vector extension with a specialized vector system if the project scale justifies both.

## Part I: Distributed data-system foundations

### Lesson 25: Partitioning

- horizontal partitioning
- partition key
- routing
- rebalancing
- hot partitions
- cross-partition operations

### Lesson 26: Replication

- replicas
- leader and follower concepts
- multi-leader concepts
- leaderless concepts
- synchronous and asynchronous replication
- failover
- replication lag

### Lesson 27: Consistency models

- strong consistency
- eventual consistency
- read-your-writes
- monotonic reads
- stale reads
- conflict resolution
- consistency at different system boundaries

### Lesson 28: Availability and network partitions

- node failure
- network partition
- availability
- consistency
- CAP theorem as a limited model
- why CAP is not a complete database-selection rule
- latency and consistency trade-offs

### Lesson 29: Distributed transactions

- atomicity across partitions
- coordination cost
- two-phase commit as a concept
- sagas as a concept
- idempotency
- compensating actions

## Part J: Cloud-managed non-relational services

### Lesson 30: Managed-service evaluation

- service abstraction
- scaling model
- pricing units
- backups
- replication
- availability targets
- identity and access
- networking
- observability
- portability

### Lesson 31: Azure Cosmos DB

- globally distributed database concepts
- supported data models and APIs
- partition keys
- request-unit-style capacity concepts
- consistency choices
- indexing
- change feed concepts
- operational and cost trade-offs

### Lesson 32: Other managed-service categories

- managed document stores
- managed key-value stores
- managed graph databases
- managed search services
- managed time-series services
- managed vector-search capabilities

### Practical milestone

Map one local specialized-data-store implementation to an Azure-managed equivalent and document the changes in security, networking, scaling, and cost responsibility.

## Part K: Polyglot persistence and system integration

### Lesson 33: Polyglot persistence

- selecting several storage systems for different responsibilities
- authoritative source
- derived stores
- duplication across systems
- ownership
- synchronization
- operational complexity

### Lesson 34: Data movement between stores

- batch replication
- change data capture concepts
- event-driven synchronization
- dual-write risk
- replay
- reconciliation
- rebuilding derived stores

### Lesson 35: Governance and lifecycle

- retention
- deletion
- personal data
- auditability
- encryption
- backup
- disaster recovery
- schema evolution
- decommissioning

### Integration milestone

Design a justified architecture in which PostgreSQL remains the transactional source of truth while selected specialized stores support caching, graph traversal, search, time-series analysis, or vector retrieval.

## Comparative project exercises

1. Model the same customer-service information in PostgreSQL and a document database.
2. Compare relational joins with document embedding and application-side composition.
3. Add Redis caching to a read-heavy service and define invalidation behavior.
4. Represent shared customer entities in a graph and compare traversal with SQL joins.
5. Index support tickets in a search engine and compare exact filtering with relevance-ranked search.
6. Store network measurements in a time-series-oriented design.
7. Implement vector similarity search and compare relational extension versus specialized service options.
8. Produce a technology decision record for each selected store.

## Completion criteria

The roadmap is complete when the learner can:

- explain the main non-relational database families
- distinguish logical data models from product names
- compare normalization, denormalization, and embedding
- model documents, key-value access, wide-column access patterns, and graphs
- explain partitioning, replication, and consistency at a practical level
- identify the limitations of CAP-based slogans
- use at least one document database, one key-value store, and one graph database
- explain search, time-series, and vector-oriented storage
- choose a storage system from workload requirements
- design synchronization and recovery between multiple stores
- document security, governance, cost, and operational trade-offs
- justify when PostgreSQL alone is sufficient
- avoid adding a specialized database when its benefits do not outweigh its complexity
