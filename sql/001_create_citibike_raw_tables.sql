BEGIN;

CREATE SCHEMA IF NOT EXISTS source;

CREATE TABLE IF NOT EXISTS source.citibike_file (
    file_id BIGINT
        GENERATED ALWAYS AS IDENTITY
        PRIMARY KEY,

    source_filename TEXT NOT NULL,

    source_sha256 TEXT NOT NULL
        UNIQUE
        CHECK (CHAR_LENGTH(source_sha256) = 64),

    source_file_size_bytes BIGINT NOT NULL
        CHECK (source_file_size_bytes >= 0),

    source_row_count INTEGER NOT NULL
        CHECK (source_row_count >= 0),

    loaded_at TIMESTAMP WITH TIME ZONE NOT NULL
        DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS source.citibike_trip_raw (
    file_id BIGINT NOT NULL
        REFERENCES source.citibike_file (file_id),

    source_row_number INTEGER NOT NULL
        CHECK (source_row_number > 0),

    ride_id TEXT,
    rideable_type TEXT,
    started_at TEXT,
    ended_at TEXT,
    start_station_name TEXT,
    start_station_id TEXT,
    end_station_name TEXT,
    end_station_id TEXT,
    start_lat TEXT,
    start_lng TEXT,
    end_lat TEXT,
    end_lng TEXT,
    member_casual TEXT,

    PRIMARY KEY (
        file_id,
        source_row_number
    )
);

COMMIT;