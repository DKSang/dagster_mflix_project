with monthly_engagement as (
    select
        date_trunc('month', cast(d.date_key as date)) as month_start,
        d.movie_id,
        sum(d.total_views) as total_views,
        sum(d.total_watch_time) as total_watch_time,
        sum(d.unique_viewers) as unique_viewers
    from {{ ref('fct_movie_consumption_daily') }} d
    group by 1, 2
),

scored as (
    select
        e.month_start,
        e.movie_id,
        m.title,
        e.total_views,
        e.total_watch_time,
        e.unique_viewers,
        (e.total_views * 1.0) + (e.total_watch_time * 0.1) + (e.unique_viewers * 2.0) as engagement_score,
        row_number() over (
            partition by e.month_start
            order by
                (e.total_views * 1.0) + (e.total_watch_time * 0.1) + (e.unique_viewers * 2.0) desc,
                e.movie_id asc
        ) as rank
    from monthly_engagement e
    inner join {{ ref('dim_movies') }} m
        on e.movie_id = m.movie_id
)

select
    month_start,
    movie_id,
    title,
    total_views,
    total_watch_time,
    unique_viewers,
    engagement_score,
    rank
from scored
where rank <= 10