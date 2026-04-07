with base as (
    select
        m.movie_id,
        c.dlt_movie_id,
        trim(c.cast_name) as cast_name,
        c.cast_ordinal
    from {{ ref('stg_movie_cast') }} c
    inner join {{ ref('stg_embedded_movies') }} m
        on c.dlt_movie_id = m.dlt_movie_id
    where nullif(trim(c.cast_name), '') is not null
),

dedup as (
    select
        movie_id,
        dlt_movie_id,
        cast_name,
        min(cast_ordinal) as cast_ordinal
    from base
    group by 1, 2, 3
)

select
    movie_id,
    dlt_movie_id,
    cast_name,
    cast_ordinal
from dedup
