-- depends_on: {{ source('dagster_quality', 'raw_quality_gate') }}

with source as (
    select *
    from {{ source('raw', 'embedded_movies') }}
)

select
    _id as movie_id,
    imdb__rating as imdb_rating,
    imdb__votes as imdb_votes,
    _dlt_id as dlt_movie_id,
    source.* exclude (_id, imdb__rating, imdb__votes, _dlt_id)
from source