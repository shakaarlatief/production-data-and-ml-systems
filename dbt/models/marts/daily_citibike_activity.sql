with trips as (
    select *
    from {{ ref('stg_citibike_trips') }}
),

daily_activity as (
    select
        ride_date,
        rideable_type,
        member_casual,
        count(*) as trip_count,
        avg(duration_minutes) as average_duration_minutes,
        sum(case when is_long_trip then 1 else 0 end) as long_trip_count,
        sum(
            case
                when has_missing_end_station then 1
                else 0
            end
        ) as missing_end_station_count,
        sum(
            case
                when has_missing_end_coordinates then 1
                else 0
            end
        ) as missing_end_coordinates_count
    from trips
    group by
        ride_date,
        rideable_type,
        member_casual
)

select *
from daily_activity
