with base as (
    select distinct
        cast(comment_date as date) as date_key
    from {{ ref('stg_comments') }}
    where comment_date is not null
)

select
    date_key,
    year(date_key) as year_number,
    month(date_key) as month_number,
    date_trunc('month', date_key) as month_start,
    dayofweek(date_key) as day_of_week_number,
    day(date_key) as day_of_month
from base