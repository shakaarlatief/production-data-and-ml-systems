select
    ride_date,
    rideable_type,
    member_casual,
    count(*) as occurrence_count
from {{ ref('daily_citibike_activity') }}
group by
    ride_date,
    rideable_type,
    member_casual
having count(*) > 1
