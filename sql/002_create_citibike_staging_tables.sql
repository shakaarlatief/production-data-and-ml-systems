BEGIN;

CREATE SCHEMA IF NOT EXISTS staging;

CREATE TABLE IF NOT EXISTS staging.citibike_trip_valid (
    file_id BIGINT NOT NULL,
    source_row_number INTEGER NOT NULL,

    ride_id TEXT NOT NULL,
    rideable_type TEXT NOT NULL
        CHECK (
            rideable_type IN (
                'classic_bike',
                'electric_bike'
            )
        ),

    started_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    ended_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    duration_seconds DOUBLE PRECISION NOT NULL
        CHECK (duration_seconds > 0),

    start_station_name TEXT NOT NULL,
    start_station_id TEXT NOT NULL,

    end_station_name TEXT,
    reported_end_station_id TEXT,
    resolved_end_station_id TEXT,
    end_station_id_resolution_method TEXT NOT NULL
        CHECK (
            end_station_id_resolution_method IN (
                'source',
                'inferred_from_station_name',
                'ambiguous_station_name',
                'unavailable'
            )
        ),

    start_lat DOUBLE PRECISION NOT NULL
        CHECK (start_lat BETWEEN -90 AND 90),
    start_lng DOUBLE PRECISION NOT NULL
        CHECK (start_lng BETWEEN -180 AND 180),
    end_lat DOUBLE PRECISION
        CHECK (end_lat IS NULL OR end_lat BETWEEN -90 AND 90),
    end_lng DOUBLE PRECISION
        CHECK (end_lng IS NULL OR end_lng BETWEEN -180 AND 180),

    member_casual TEXT NOT NULL
        CHECK (
            member_casual IN (
                'member',
                'casual'
            )
        ),

    is_long_trip BOOLEAN NOT NULL,
    has_missing_end_station BOOLEAN NOT NULL,
    has_missing_end_coordinates BOOLEAN NOT NULL,

    validated_at TIMESTAMP WITH TIME ZONE NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (
        file_id,
        source_row_number
    ),

    UNIQUE (ride_id),

    FOREIGN KEY (
        file_id,
        source_row_number
    )
        REFERENCES source.citibike_trip_raw (
            file_id,
            source_row_number
        )
        ON DELETE CASCADE,

    CHECK (
        (end_lat IS NULL AND end_lng IS NULL)
        OR
        (end_lat IS NOT NULL AND end_lng IS NOT NULL)
    )
);

CREATE TABLE IF NOT EXISTS staging.citibike_trip_rejected (
    file_id BIGINT NOT NULL,
    source_row_number INTEGER NOT NULL,
    ride_id TEXT,
    rejection_reasons TEXT[] NOT NULL
        CHECK (CARDINALITY(rejection_reasons) > 0),
    rejected_at TIMESTAMP WITH TIME ZONE NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (
        file_id,
        source_row_number
    ),

    FOREIGN KEY (
        file_id,
        source_row_number
    )
        REFERENCES source.citibike_trip_raw (
            file_id,
            source_row_number
        )
        ON DELETE CASCADE
);

COMMIT;
