with base as (
    select
        m.movie_id,
        g.dlt_movie_id,
        trim(g.genre_name) as genre_name,
        g.genre_ordinal
    from {{ ref('stg_movie_genres') }} g
    inner join {{ ref('stg_embedded_movies') }} m
        on g.dlt_movie_id = m.dlt_movie_id
    where nullif(trim(g.genre_name), '') is not null
),

dedup as (
    select
        movie_id,
        dlt_movie_id,
        genre_name,
        min(genre_ordinal) as genre_ordinal
    from base
    group by 1, 2, 3
)

select
    movie_id,
    dlt_movie_id,
    genre_name,
    genre_ordinal
from dedup
