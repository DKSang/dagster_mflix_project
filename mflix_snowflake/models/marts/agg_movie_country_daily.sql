with daily_comments as (
    select
        movie_id,
        cast(comment_date as date) as date_key,
        count(*) as total_views,
        sum(coalesce(length(trim(comment_text)), 0)) as total_watch_time,
        count(distinct commenter_email) as unique_viewers
    from {{ ref('stg_comments') }}
    where movie_id is not null
      and comment_date is not null
    group by 1, 2
),

movie_country as (
    select
        movie_id,
        primary_country_name
    from {{ ref('int_movie_flattened') }}
    where primary_country_name is not null
),

base as (
    select
        d.movie_id,
        d.date_key,
        c.country_key,
        c.country_code,
        c.country_name,
        d.total_views,
        d.total_watch_time,
        d.unique_viewers
    from daily_comments d
    inner join movie_country m
        on d.movie_id = m.movie_id
    inner join {{ ref('dim_country') }} c
        on m.primary_country_name = c.country_name
)

select
    movie_id,
    date_key,
    country_key,
    country_code,
    country_name,
    total_views,
    total_watch_time,
    unique_viewers
from base