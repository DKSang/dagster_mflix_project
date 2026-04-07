with source as (
    select
        movie_id,
        cast(comment_date as date) as date_key,
        comment_date as event_ts,
        commenter_email,
        trim(comment_text) as comment_text
    from {{ ref('stg_comments') }}
    where movie_id is not null
      and comment_date is not null
),

daily as (
    select
        movie_id,
        date_key,
        count(*) as total_views,
        sum(coalesce(length(comment_text), 0)) as total_watch_time,
        count(distinct commenter_email) as unique_viewers,
        1.0 * count_if(comment_text is not null) / nullif(count(*), 0) as completion_rate,
        1.0 * sum(coalesce(length(comment_text), 0)) / nullif(count(*), 0) as avg_watch_time,
        min(event_ts) as first_event_ts,
        max(event_ts) as last_event_ts
    from source
    group by 1, 2
)

select
    movie_id,
    date_key,
    total_views,
    total_watch_time,
    unique_viewers,
    completion_rate,
    avg_watch_time,
    first_event_ts,
    last_event_ts
from daily