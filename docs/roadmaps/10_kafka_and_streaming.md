# Roadmap: Kafka and Streaming Systems

## Objective

Understand event-driven data movement and build a reliable small streaming pipeline.

## Prerequisites

- data pipeline foundations
- basic networking
- serialization formats
- storage concepts
- distributed systems introduction

## Part A: Event foundations

1. event
2. event payload
3. event key
4. event time
5. processing time
6. schema
7. immutable event log
8. command versus event
9. batch versus streaming
10. use-case selection

## Part B: Kafka architecture

1. broker
2. cluster
3. topic
4. partition
5. offset
6. producer
7. consumer
8. consumer group
9. replication
10. retention

## Part C: Delivery and ordering

1. ordering within a partition
2. keys and partition selection
3. at-most-once
4. at-least-once
5. effectively-once designs
6. duplicates
7. idempotent consumers
8. acknowledgements
9. retries
10. dead-letter handling

## Part D: Schemas and compatibility

1. JSON limitations
2. Avro or similar schema-based formats
3. schema registry concepts
4. backward compatibility
5. forward compatibility
6. evolution
7. validation
8. versioning

## Part E: Stream processing

1. stateless transformations
2. stateful processing
3. windows
4. aggregations
5. joins
6. late events
7. watermarks
8. checkpoints
9. replay
10. materialized results

## Part F: Integration

1. writing events to storage
2. change data capture concepts
3. connectors
4. streaming features
5. real-time predictions
6. monitoring lag
7. scaling consumers
8. failure recovery

## Practical milestones

- run a local Kafka environment
- publish telecom usage and support events
- consume events with explicit offsets
- demonstrate consumer groups
- handle duplicates safely
- validate event schemas
- write events to analytical storage
- build a small rolling metric

## Completion criteria

- can explain topics, partitions, offsets, and consumer groups
- can reason about ordering and delivery guarantees
- can build idempotent consumers
- can handle schema evolution
- can distinguish a justified streaming use case from unnecessary complexity
