# Citi Bike ETL Case Study

## Purpose

This case study provides the first practical implementation of a local, transparent data pipeline using Python, PostgreSQL, dbt Core, and a real public dataset.

It is a focused learning implementation within the wider production data and machine-learning systems programme. It is distinct from the long-term telecommunications integrated project described in `03_integrated_project_architecture.md`.

The implementation is intentionally layered. Direct Python, the standard library, Psycopg 3, PostgreSQL, and explicit SQL are used first so that file ingestion, database interaction, transactions, validation, and lineage remain visible. dbt Core is then introduced for dependency-aware analytical transformations, data tests, materializations, and generated documentation. Orchestration, containers, distributed processing, and cloud services remain later phases.

## Why Citi Bike was selected

The Citi Bike trip-history archive provides a realistic foundation for learning data engineering because it combines several useful properties:

- official real-world source data;
- recurring time-partitioned files;
- identifiers, categories, timestamps, coordinates, and station information;
- moderate local-development files and much larger files for later scalability work;
- natural data-quality questions;
- clear analytical outputs;
- a future path from batch files to API-based ingestion.

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

Preserving this grain is important during extraction, raw landing, validation, and the first dbt staging model. The analytical mart intentionally changes the grain to one row per ride date, bicycle type, and membership category.

## Source inspection and profiling

The January 2025 Jersey City file contains:

- 50,611 data rows;
- 13 columns.

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

- all 50,611 non-missing ride identifiers are unique;
- no completely identical source rows were found;
- `rideable_type` contains `electric_bike` and `classic_bike`;
- `member_casual` contains `member` and `casual`;
- all start and end timestamps parse successfully;
- no trip has a nonpositive duration;
- 21 trips exceed 24 hours and are retained as soft quality conditions;
- two trips begin shortly before midnight on 31 December 2024 and end after midnight on 1 January 2025;
- all non-missing coordinates are finite and within geographic latitude and longitude ranges;
- 25 rows contain an end-station name but no end-station identifier;
- each of those 25 station names maps uniquely to one identifier observed elsewhere in the source data;
- 107 rows have no resolved end-station identifier;
- 19 rows have neither end coordinate;
- station identifier `JC075` appears with both `Monmouth and 6th` and `Monmouth & 6th`.

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
          dbt source()
              |
              v
analytics.stg_citibike_trips
        ride-level view
              |
              v
            dbt ref()
              |
              v
analytics.daily_citibike_activity
        daily summary table
```

The local PostgreSQL database is:

`bike_share_etl`

The schemas are:

- `source`;
- `staging`;
- `analytics`;
- `operations`.

## Raw landing layer

### `source.citibike_file`

Grain:

`one row per distinct raw source file`

The table records:

- generated file identifier;
- source filename;
- SHA-256 content hash;
- file size in bytes;
- source row count;
- load timestamp.

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

- typed start and end timestamps;
- calculated trip duration in seconds;
- typed geographic coordinates;
- reported and resolved end-station identifiers;
- an explicit end-station resolution method;
- soft quality flags;
- source lineage through `file_id` and `source_row_number`.

The accepted table preserves the distinction between provider-supplied and inferred station identifiers:

- `reported_end_station_id` contains the original source value;
- `resolved_end_station_id` contains the usable identifier after deterministic resolution;
- `end_station_id_resolution_method` records whether the value came from the source, was inferred from a unique station-name match, was ambiguous, or remained unavailable.

### `staging.citibike_trip_rejected`

Grain:

`one row per rejected raw source row`

Each rejected record retains source lineage and an array of one or more explicit rejection reasons. This design allows one source row to fail several independent rules while remaining traceable to the original raw record.

## Validation policy

### Hard rejection conditions

A record is rejected when it cannot represent a technically valid typed trip. Examples include:

- missing ride identifier;
- duplicate accepted ride identifier;
- missing or unknown bicycle type;
- missing or unknown membership type;
- missing or invalid timestamps;
- end time not later than start time;
- missing start-station information;
- missing, nonfinite, or geographically invalid start coordinates;
- malformed or geographically invalid end coordinates;
- only one member of an end-coordinate pair being present.

### Soft quality conditions

The following conditions do not make the entire trip unusable:

- duration longer than 24 hours;
- missing end-station identifier that can be inferred deterministically;
- unresolved end-station information;
- missing end coordinates;
- a ride beginning just outside the nominal month boundary;
- station-name variation for the same station identifier.

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

## Automated Python validation

A controlled synthetic fixture under `tests/fixtures/` verifies deterministic behavior for cases such as:

- duplicate ride identifiers;
- invalid timestamp strings;
- an end timestamp before a start timestamp;
- missing required values;
- invalid categorical values;
- latitude or longitude outside valid ranges;
- malformed numeric values;
- incomplete coordinate pairs;
- deterministic and ambiguous station resolution;
- soft quality conditions.

Verified result:

```text
12 passed
All checks passed!
```

Synthetic fixtures remain separate from the real raw dataset and are never presented as real Citi Bike observations.

## Pipeline-run audit structure

### `operations.pipeline_run`

Grain:

`one row per execution of one pipeline stage`

The table records stage identity, status, timestamps, row counts, optional file lineage, error details, and supplementary `JSONB` metadata. Database constraints prevent contradictory states, such as a completed run without a finish timestamp.

The table exists and has been verified in PostgreSQL. It is currently empty because the Python programs do not yet write run records automatically.

## dbt Core analytical transformation layer

The dbt project is configured through:

- `dbt_project.yml`;
- `dbt/profiles.yml`.

The PostgreSQL target reads connection values from environment variables. Local credentials therefore remain in the ignored `.env` file rather than being committed.

### dbt sources

The existing PostgreSQL staging tables are declared as dbt sources:

- logical source `citibike.trip_valid` resolves to `staging.citibike_trip_valid`;
- logical source `citibike.trip_rejected` resolves to `staging.citibike_trip_rejected`.

`source()` both resolves the physical relation name and records upstream lineage.

### `analytics.stg_citibike_trips`

Model file:

`dbt/models/staging/stg_citibike_trips.sql`

Materialization:

`view`

Grain:

`one row per accepted bicycle ride`

The model reads from `citibike.trip_valid` and adds:

- `ride_date`, derived from `started_at`;
- `start_hour`, extracted from `started_at`;
- `duration_minutes`, calculated from `duration_seconds`.

No filtering, grouping, or joining occurs, so the ride-level grain and 50,611-row count are preserved.

### `analytics.daily_citibike_activity`

Model file:

`dbt/models/marts/daily_citibike_activity.sql`

Materialization:

`table`

Grain:

`one row per ride date, bicycle type, and membership category`

The model depends on `stg_citibike_trips` through:

```sql
{{ ref('stg_citibike_trips') }}
```

`ref()` resolves the environment-specific database relation and records the dependency used by dbt's directed acyclic graph.

The mart stores:

- `trip_count`;
- `average_duration_minutes`;
- `long_trip_count`;
- `missing_end_station_count`;
- `missing_end_coordinates_count`.

Staging models are configured as views, while mart models are configured as tables. This preserves a lightweight ride-level interface and stores the repeatedly queried aggregation physically.

## dbt data tests

### Generic tests

YAML-defined generic tests cover:

- `not_null`;
- `unique`;
- `accepted_values`.

These tests protect source and model assumptions such as unique ride identifiers, required timestamps, and accepted category values.

### Singular tests

Project-specific SQL tests under `dbt/tests/` verify:

1. the declared daily mart grain is unique;
2. counts and averages remain within logically valid bounds;
3. `sum(trip_count)` reconciles with the ride-level row count.

A singular test returns invalid records. Zero returned rows means the test passes.

Verified selected dependency-chain build:

```text
Found 2 models, 34 data tests, 2 sources
Finished running 31 data tests, 2 models
PASS=33 WARN=0 ERROR=0 SKIP=0 TOTAL=33
```

The three generic tests attached only to the rejected-record source were not selected because that source is not an upstream dependency of the daily mart.

## dbt documentation and lineage

`dbt docs generate` produced local documentation artifacts under the ignored `target/` directory. `dbt docs serve` exposed the documentation through a local browser interface.

The verified lineage graph shows:

```text
citibike.trip_valid
        -> stg_citibike_trips
        -> daily_citibike_activity
        -> grain, measure-bound, and reconciliation tests
```

`citibike.trip_rejected` appears as a separate source without a downstream analytical model. This accurately represents the current project graph.

The generated interface also exposes model descriptions, column descriptions, data types, materializations, tests, compiled SQL, and upstream and downstream relationships.

## Reliability properties implemented

The local pipeline now demonstrates:

- immutable raw source handling;
- schema-drift detection;
- file identity through SHA-256 hashing;
- transactional raw ingestion;
- bulk loading with PostgreSQL `COPY`;
- raw source lineage;
- deterministic rerun behavior;
- explicit accepted and rejected outcomes;
- hard validation versus soft quality flags;
- source-to-staging row-count reconciliation;
- preservation of reported and inferred values;
- automated unit tests for validation logic;
- dependency-aware SQL transformations;
- explicit model grains;
- view and table materialization strategies;
- generic and project-specific dbt data tests;
- analytical reconciliation;
- generated documentation and lineage.

## Current progress

Completed:

- Python 3.11 virtual environment created;
- Psycopg 3 and python-dotenv installed;
- local secrets separated through an ignored `.env` file;
- Python-to-PostgreSQL connection verified;
- `bike_share_etl` database created;
- `source`, `staging`, `analytics`, and `operations` schemas created;
- official January 2025 Jersey City trip data downloaded;
- raw-data directory excluded from Git;
- source structure, missingness, categories, identifiers, timestamps, durations, coordinates, and station mappings profiled;
- raw manifest and raw trip tables created;
- 50,611 source rows loaded transactionally;
- SHA-256-based idempotent raw rerun verified;
- accepted and rejected staging tables created;
- typed validation pipeline implemented;
- deterministic station-ID inference implemented without overwriting source values;
- source-to-staging reconciliation verified;
- validation rerun behavior verified;
- controlled automated validation tests implemented;
- pipeline-run audit table created and verified;
- dbt Core and the PostgreSQL adapter installed;
- environment-based dbt connection verified;
- staging tables declared as dbt sources;
- ride-level staging view built and tested;
- daily analytical mart table built and tested;
- custom grain, bounds, and reconciliation tests implemented;
- generated dbt documentation and lineage verified.

## Immediate next steps

1. Introduce Docker images, containers, registries, ports, networks, and volumes.
2. Define a PostgreSQL service without modifying the existing local database installation.
3. Use Docker Compose for reproducible multi-service configuration.
4. Add persistent named volumes and database health checks.
5. connect the existing Python and dbt workflows to containerized PostgreSQL;
6. verify startup, shutdown, rebuild, and persistence behavior;
7. add orchestration and continuous integration only after the containerized local environment is stable.

## Scope boundary

This case study currently covers a local batch ETL and analytics-engineering workflow. It does not yet include:

- containers;
- workflow orchestration;
- cloud storage or cloud databases;
- distributed processing;
- streaming ingestion;
- machine-learning training;
- deployment;
- production monitoring.

Those capabilities will be introduced later when the local implementation provides concrete requirements and reusable foundations.
