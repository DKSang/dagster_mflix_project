with base as (
    select
        m.movie_id,
        l.dlt_movie_id,
        trim(l.language_name) as language_name,
        l.language_ordinal
    from {{ ref('stg_movie_languages') }} l
    inner join {{ ref('stg_embedded_movies') }} m
        on l.dlt_movie_id = m.dlt_movie_id
    where nullif(trim(l.language_name), '') is not null
),

dedup as (
    select
        movie_id,
        dlt_movie_id,
        language_name,
        min(language_ordinal) as language_ordinal
    from base
    group by 1, 2, 3
)

select
    movie_id,
    dlt_movie_id,
    language_name,
    language_ordinal
from dedup
