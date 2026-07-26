select
    ride_date,
    rideable_type,
    member_casual,
    trip_count,
    average_duration_minutes,
    long_trip_count,
    missing_end_station_count,
    missing_end_coordinates_count
from {{ ref('daily_citibike_activity') }}
where
    trip_count <= 0
    or average_duration_minutes <= 0
    or long_trip_count < 0
    or missing_end_station_count < 0
    or missing_end_coordinates_count < 0
    or long_trip_count > trip_count
    or missing_end_station_count > trip_count
    or missing_end_coordinates_count > trip_count
