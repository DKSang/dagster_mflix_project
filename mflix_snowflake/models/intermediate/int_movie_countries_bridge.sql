with base as (
    select
        m.movie_id,
        c.dlt_movie_id,
        trim(c.country_name) as country_name,
        c.country_ordinal
    from {{ ref('stg_movie_countries') }} c
    inner join {{ ref('stg_embedded_movies') }} m
        on c.dlt_movie_id = m.dlt_movie_id
    where nullif(trim(c.country_name), '') is not null
),

dedup as (
    select
        movie_id,
        dlt_movie_id,
        country_name,
        min(country_ordinal) as country_ordinal
    from base
    group by 1, 2, 3
)

select
    movie_id,
    dlt_movie_id,
    country_name,
    country_ordinal
from dedup
