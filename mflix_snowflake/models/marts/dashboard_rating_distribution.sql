{{ config(materialized='view') }}

select
    q.rating_bucket,
    count(*) as movie_count,
    avg(q.imdb_rating) as avg_imdb_rating,
    sum(q.imdb_votes) as total_imdb_votes
from {{ ref('fct_movie_quality') }} q
group by 1
