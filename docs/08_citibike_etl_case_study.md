# Citi Bike ETL Case Study

## Purpose

This case study provides the first practical implementation of a local, transparent ETL pipeline using Python, PostgreSQL, and a real public dataset.

It is a focused learning implementation within the wider production data and machine-learning systems programme. It is distinct from the long-term telecommunications integrated project described in `03_integrated_project_architecture.md`.

The implementation is intended to make each stage visible before higher-level abstractions are introduced. Direct Python, the standard library, Psycopg 3, PostgreSQL, and explicit SQL are therefore used first. Orchestration, warehouse tooling, containers, distributed processing, and cloud services will be added only after the underlying responsibilities are understood.

## Why Citi Bike was selected

The Citi Bike trip-history archive provides a realistic foundation for learning data engineering because it combines several useful properties:

- official real-world source data
- recurring time-partitioned files
- identifiers, categories, timestamps, coordinates, and station information
- moderate local-development files and much larger files for later scalability work
- natural data-quality questions
- clear analytical outputs
- a future path from batch files to API-based ingestion

The case study uses real Citi Bike data as the primary source. Synthetic data is limited to clearly identified test fixtures that create controlled failure cases which may not occur reliably in the real source.

## Initial data source

The first development source is the January 2025 Jersey City Citi Bike trip-history archive:

`JC-202501-citibike-tripdata.csv.zip`

The extracted source file is:

`JC-202501-citibike-tripdata.csv`

Raw files are stored locally under:

`data/raw/citibike/`

The `data/raw/` directory is excluded from Git. The repository preserves the code and instructions needed to obtain and process the source rather than duplicating the raw dataset.

Raw files are treated as immutable inputs. They are not manually edited or cleaned in place.

## Source grain

The source grain is:

`one row per recorded bicycle ride`

Preserving this grain is important during extraction, raw landing, and staging. Analytical transformations may later create other grains, such as one row per station per day, but that change must be explicit.

## Source inspection and profiling

The January 2025 Jersey City file contains:

- 50,611 data rows
- 13 columns

The source columns are:

1. `ride_id`
2. `rideable_type`
3. `started_at`
4. `ended_at`
5. `start_station_name`
6. `start_station_id`
7. `end_station_name`
8. `end_station_id`
9. `start_lat`
10. `start_lng`
11. `end_lat`
12. `end_lng`
13. `member_casual`

The initial CSV reader treats every source value as text. Parsing into timestamps, numeric values, categories, and database nulls belongs to the transformation and validation stages.

### Missing-value profile

| Column | Missing rows | Missing percentage |
|---|---:|---:|
| `end_station_name` | 107 | 0.21% |
| `end_station_id` | 132 | 0.26% |
| `end_lat` | 19 | 0.04% |
| `end_lng` | 19 | 0.04% |

No missing values were observed in the remaining columns.

### Deeper profiling findings

- all 50,611 non-missing ride identifiers are unique
- no completely identical source rows were found
- `rideable_type` contains `electric_bike` and `classic_bike`
- `member_casual` contains `member` and `casual`
- all start and end timestamps parse successfully
- no trip has a nonpositive duration
- 21 trips exceed 24 hours and are retained as soft quality conditions
- two trips begin shortly before midnight on 31 December 2024 and end after midnight on 1 January 2025
- all non-missing coordinates are finite and within geographic latitude and longitude ranges
- 25 rows contain an end-station name but no end-station identifier
- each of those 25 station names maps uniquely to one identifier observed elsewhere in the source data
- 107 rows have no resolved end-station identifier
- 19 rows have neither end coordinate
- station identifier `JC075` appears with both `Monmouth and 6th` and `Monmouth & 6th`

These findings distinguish unusual but usable records from records that would be technically invalid.

## Local architecture

```text
Official Citi Bike ZIP archive
              |
              v
Local immutable raw file
              |
              v
source.citibike_file
source.citibike_trip_raw
              |
              v
Python parsing and validation
              |
              v
staging.citibike_trip_valid
staging.citibike_trip_rejected
              |
              v
Planned analytical models
              |
              v
PostgreSQL analytics layer
```

The local PostgreSQL database is:

`bike_share_etl`

The schemas are:

- `source`
- `staging`
- `analytics`

## Raw landing layer

### `source.citibike_file`

Grain:

`one row per distinct raw source file`

The table records:

- generated file identifier
- source filename
- SHA-256 content hash
- file size in bytes
- source row count
- load timestamp

The SHA-256 hash is unique. Reprocessing the same file content therefore does not create a second manifest record or duplicate raw rows.

### `source.citibike_trip_raw`

Grain:

`one row per CSV data row per source file`

The primary key is:

`(file_id, source_row_number)`

All thirteen source fields are stored as text. This is deliberate: the raw layer preserves what arrived even when a future source value cannot be parsed into a target type.

The January file was loaded with PostgreSQL `COPY` inside one transaction. The result was:

| Measure | Count |
|---|---:|
| Manifest source row count | 50,611 |
| Raw database row count | 50,611 |
| Counts match | true |

A second execution detected the existing SHA-256 hash and inserted no duplicate rows.

## Validated staging layer

### `staging.citibike_trip_valid`

Grain:

`one row per accepted raw source row`

The table contains parsed and validated values, including:

- typed start and end timestamps
- calculated trip duration in seconds
- typed geographic coordinates
- reported and resolved end-station identifiers
- an explicit end-station resolution method
- soft quality flags
- source lineage through `file_id` and `source_row_number`

The accepted table preserves the distinction between provider-supplied and inferred station identifiers:

- `reported_end_station_id` contains the original source value
- `resolved_end_station_id` contains the usable identifier after deterministic resolution
- `end_station_id_resolution_method` records whether the value came from the source, was inferred from a unique station-name match, was ambiguous, or remained unavailable

### `staging.citibike_trip_rejected`

Grain:

`one row per rejected raw source row`

Each rejected record retains source lineage and an array of one or more explicit rejection reasons. This design allows one source row to fail several independent rules while remaining traceable to the original raw record.

## Validation policy

### Hard rejection conditions

A record is rejected when it cannot represent a technically valid typed trip. Examples include:

- missing ride identifier
- duplicate accepted ride identifier
- missing or unknown bicycle type
- missing or unknown membership type
- missing or invalid timestamps
- end time not later than start time
- missing start-station information
- missing, nonfinite, or geographically invalid start coordinates
- malformed or geographically invalid end coordinates
- only one member of an end-coordinate pair being present

### Soft quality conditions

The following conditions do not make the entire trip unusable:

- duration longer than 24 hours
- missing end-station identifier that can be inferred deterministically
- unresolved end-station information
- missing end coordinates
- a ride beginning just outside the nominal month boundary
- station-name variation for the same station identifier

Soft conditions are preserved through explicit fields or flags rather than causing silent deletion.

## Staging validation result

The January file was validated twice to test deterministic rerun behavior. Both executions produced the same result:

| Measure | Count |
|---|---:|
| Raw rows | 50,611 |
| Valid rows | 50,611 |
| Rejected rows | 0 |
| Reconciliation | 50,611 + 0 = 50,611 |

Observed quality flags among accepted rows:

| Quality flag | Count |
|---|---:|
| Missing resolved end station | 107 |
| End-station identifier inferred from station name | 25 |
| Trip longer than 24 hours | 21 |
| Missing end coordinates | 19 |

The second validation execution replaced the selected file's staging outcomes transactionally and reproduced the same counts without appending duplicates.

## Reliability properties implemented

The local pipeline now demonstrates:

- immutable raw source handling
- schema-drift detection
- file identity through SHA-256 hashing
- transactional raw ingestion
- bulk loading with PostgreSQL `COPY`
- raw source lineage
- deterministic rerun behavior
- explicit accepted and rejected outcomes
- hard validation versus soft quality flags
- source-to-staging row-count reconciliation
- preservation of reported and inferred values

## Synthetic test data policy

Synthetic records may be introduced only as clearly labelled test fixtures. Their purpose is to verify deterministic behavior for cases such as:

- duplicate ride identifiers
- invalid timestamp strings
- an end timestamp before a start timestamp
- missing required values
- invalid categorical values
- latitude or longitude outside valid ranges
- malformed numeric values
- incomplete coordinate pairs
- repeated loading of the same source file

Synthetic fixtures must not be mixed with the real raw dataset or presented as real Citi Bike observations.

## Current progress

Completed:

- Python 3.11 virtual environment created
- Psycopg 3 and python-dotenv installed
- local secrets separated through an ignored `.env` file
- Python-to-PostgreSQL connection verified
- `bike_share_etl` database created
- `source`, `staging`, and `analytics` schemas created
- official January 2025 Jersey City trip data downloaded
- raw-data directory excluded from Git
- source structure, missingness, categories, identifiers, timestamps, durations, coordinates, and station mappings profiled
- raw manifest and raw trip tables created
- 50,611 source rows loaded transactionally
- SHA-256-based idempotent raw rerun verified
- accepted and rejected staging tables created
- typed validation pipeline implemented
- deterministic station-ID inference implemented without overwriting source values
- source-to-staging reconciliation verified
- validation rerun behavior verified

## Immediate next steps

1. Add automated tests with controlled synthetic fixtures for each hard rejection rule.
2. Add structured logging and persistent pipeline-run metadata.
3. Centralize shared configuration and database-connection code.
4. Design analytical trip and station models with explicit grains.
5. Build the first analytics-layer transformation from validated staging records.
6. Add a second monthly source file to test multi-file behavior and cross-file uniqueness.
7. Introduce reproducible dependency metadata and code-quality tooling.

## Scope boundary

This case study currently covers a local batch ETL workflow. It does not yet include:

- workflow orchestration
- cloud storage or cloud databases
- containers
- distributed processing
- streaming ingestion
- machine-learning training
- deployment
- production monitoring

Those capabilities will be introduced later when the local implementation provides concrete requirements and reusable foundations.
