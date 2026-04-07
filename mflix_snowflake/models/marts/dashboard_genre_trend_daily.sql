{{ config(materialized='view') }}

with base as (
    select
        c.date_key,
        e.primary_genre_id,
        c.total_views,
        c.total_watch_time,
        c.unique_viewers
    from {{ ref('fct_movie_consumption_daily') }} c
    inner join {{ ref('fct_movie_engagement') }} e
        on c.movie_id = e.movie_id
),
aggregated as (
    select
        date_key,
        primary_genre_id,
        sum(total_views) as total_views,
        sum(total_watch_time) as total_watch_time,
        sum(unique_viewers) as unique_viewers
    from base
    group by 1, 2
)
select
    a.date_key,
    a.primary_genre_id as genre_id,
    g.genre_name,
    a.total_views,
    a.total_watch_time,
    a.unique_viewers
from aggregated a
left join {{ ref('dim_genres') }} g
    on a.primary_genre_id = g.genre_id
