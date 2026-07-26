with ride_level as (
    select count(*) as ride_count
    from {{ ref('stg_citibike_trips') }}
),

daily_summary as (
    select sum(trip_count) as summarized_ride_count
    from {{ ref('daily_citibike_activity') }}
)

select
    ride_level.ride_count,
    daily_summary.summarized_ride_count
from ride_level
cross join daily_summary
where ride_level.ride_count <> daily_summary.summarized_ride_count
