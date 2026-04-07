with base as (
    select
        m.movie_id,
        d.dlt_movie_id,
        trim(d.director_name) as director_name,
        d.director_ordinal
    from {{ ref('stg_movie_directors') }} d
    inner join {{ ref('stg_embedded_movies') }} m
        on d.dlt_movie_id = m.dlt_movie_id
    where nullif(trim(d.director_name), '') is not null
),

dedup as (
    select
        movie_id,
        dlt_movie_id,
        director_name,
        min(director_ordinal) as director_ordinal
    from base
    group by 1, 2, 3
)

select
    movie_id,
    dlt_movie_id,
    director_name,
    director_ordinal
from dedup
