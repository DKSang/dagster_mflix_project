{{ config(materialized='view') }}

select
    month_start,
    movie_id,
    title,
    imdb_rating,
    imdb_votes
from {{ ref('agg_top_movies_by_month') }}
