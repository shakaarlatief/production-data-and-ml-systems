with valid_trips as (
    select *
    from {{ source('citibike', 'trip_valid') }}
),

prepared_trips as (
    select
        file_id,
        source_row_number,
        ride_id,
        rideable_type,
        started_at,
        ended_at,
        started_at::date as ride_date,
        extract(hour from started_at)::integer as start_hour,
        duration_seconds,
        duration_seconds / 60.0 as duration_minutes,
        start_station_name,
        start_station_id,
        end_station_name,
        reported_end_station_id,
        resolved_end_station_id,
        end_station_id_resolution_method,
        start_lat,
        start_lng,
        end_lat,
        end_lng,
        member_casual,
        is_long_trip,
        has_missing_end_station,
        has_missing_end_coordinates,
        validated_at
    from valid_trips
)

select *
from prepared_trips
