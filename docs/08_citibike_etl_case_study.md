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

The case study will use real Citi Bike data as the primary source. Synthetic data will be limited to clearly identified test fixtures that create controlled failure cases which may not occur reliably in the real source.

## Initial data source

The first development source is the January 2025 Jersey City Citi Bike trip-history archive:

`JC-202501-citibike-tripdata.csv.zip`

The extracted source file is:

`JC-202501-citibike-tripdata.csv`

Raw files are stored locally under:

`data/raw/citibike/`

The `data/raw/` directory is excluded from Git. The repository should preserve the code and instructions needed to obtain and process the source, not duplicate the raw dataset.

Raw files are treated as immutable inputs. They are not manually edited or cleaned in place.

## Source grain

The source grain is:

`one row per recorded bicycle ride`

Preserving this grain is important during extraction and staging. Analytical transformations may later create other grains, such as one row per station per day, but that change must be explicit.

## Initial source inspection

The January 2025 Jersey City file contains:

- 50,611 data rows
- 13 columns

The columns are:

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

The initial Python inspection reads every CSV cell as text. Parsing into timestamps, numeric values, categories, and database nulls belongs to the transformation and validation stages.

## Initial missing-value profile

Observed missing values:

| Column | Missing rows | Missing percentage |
|---|---:|---:|
| `end_station_name` | 107 | 0.21% |
| `end_station_id` | 132 | 0.26% |
| `end_lat` | 19 | 0.04% |
| `end_lng` | 19 | 0.04% |

No missing values were observed in the remaining columns during the initial inspection.

These findings are descriptive evidence from one file. They are not yet permanent source contracts. Additional profiling and later monthly files may reveal new values, missingness patterns, or schema changes.

## Local architecture

```text
Official Citi Bike ZIP archive
              |
              v
Local immutable raw file
              |
              v
Python extraction and validation
              |
              v
PostgreSQL staging layer
              |
              v
Validated transformations
              |
              v
PostgreSQL analytics layer
```

The local PostgreSQL database is:

`bike_share_etl`

The initial schemas are:

- `source`
- `staging`
- `analytics`

The exact role of each schema and the final table design will be refined as the pipeline is implemented. Table definitions must be derived from observed source properties and explicit processing requirements rather than from invented assumptions.

## Planned pipeline stages

1. Discover and identify an input file.
2. Record source-file metadata.
3. Read records without modifying the raw file.
4. Preserve the source row grain during extraction.
5. Parse text values into explicit Python and PostgreSQL data types.
6. Validate required fields and allowed categorical values.
7. Validate timestamps and calculate trip duration.
8. Detect duplicate ride identifiers.
9. Validate coordinate ranges.
10. Classify valid and rejected records.
11. Load records transactionally into PostgreSQL.
12. Reconcile source, valid, rejected, and loaded row counts.
13. Support safe reruns without duplicating data.
14. Add structured logging and automated tests.
15. Construct reusable analytical station and trip datasets.

## Initial quality rules under consideration

The following rules are provisional and must be confirmed through further profiling and source interpretation:

- `ride_id` must be present.
- `started_at` and `ended_at` must be parseable timestamps.
- `ended_at` must occur after `started_at`.
- trip duration should fall within a justified range.
- `rideable_type` must belong to an accepted set.
- `member_casual` must belong to an accepted set.
- latitude must fall between -90 and 90.
- longitude must fall between -180 and 180.
- duplicate ride identifiers must be handled deterministically.
- missing end-station information must be handled explicitly rather than silently discarded.
- relationships between missing station identifiers, names, and coordinates should be profiled before a rejection rule is chosen.

A source record should not be rejected merely because a value is inconvenient. Every rejection condition needs a technical or analytical justification.

## Synthetic test data policy

Synthetic records may be introduced later only as clearly labelled test fixtures. Their purpose is to verify deterministic behavior for cases such as:

- duplicate ride identifiers
- invalid timestamp strings
- an end timestamp before a start timestamp
- missing required values
- invalid categorical values
- latitude or longitude outside valid ranges
- malformed numeric values
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
- source structure, row count, example values, and missingness inspected

## Immediate next steps

1. Profile identifier uniqueness and duplicate records.
2. Profile distinct categorical values and their frequencies.
3. Parse timestamps and inspect duration distributions and invalid ordering.
4. Parse coordinates and inspect numeric validity and geographic ranges.
5. Examine relationships among missing end-station fields.
6. define the first accepted-record and rejected-record rules.
7. design the staging tables from the profiling evidence.
8. implement the first transparent extraction and transactional load.
9. verify row-count reconciliation and rerun behavior.

## Scope boundary

This case study currently covers a local batch ETL workflow. It does not yet include:

- orchestration
- cloud storage or cloud databases
- containers
- distributed processing
- streaming ingestion
- machine-learning training
- deployment
- production monitoring

Those capabilities will be introduced later when the local implementation provides concrete requirements and reusable foundations.
