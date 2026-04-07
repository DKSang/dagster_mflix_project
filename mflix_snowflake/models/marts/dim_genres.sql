with base as (
    select distinct
        genre_name
    from {{ ref('int_movie_genres_bridge') }}
    where genre_name is not null
)

select
    row_number() over (order by genre_name) as genre_id,
    genre_name
from base
