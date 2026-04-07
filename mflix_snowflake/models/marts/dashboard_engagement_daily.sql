{{ config(materialized='view') }}

select
    d.date_key,
    d.movie_id,
    m.title,
    d.total_views,
    d.total_watch_time,
    d.unique_viewers,
    d.completion_rate,
    d.avg_watch_time,
    d.first_event_ts,
    d.last_event_ts
from {{ ref('fct_movie_consumption_daily') }} d
inner join {{ ref('dim_movies') }} m
    on d.movie_id = m.movie_id
