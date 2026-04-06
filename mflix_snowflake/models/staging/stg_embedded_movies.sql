with source as (
    select *
    from {{ source('raw', 'embedded_movies') }}
)

select
    _id as movie_id,
    imdb__rating as imdb_rating,
    imdb__votes as imdb_votes,
    source.* exclude (_id, imdb__rating, imdb__votes)
from source