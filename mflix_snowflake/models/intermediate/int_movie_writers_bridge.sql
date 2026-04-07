with base as (
    select
        m.movie_id,
        w.dlt_movie_id,
        trim(w.writer_name) as writer_name,
        w.writer_ordinal
    from {{ ref('stg_movie_writers') }} w
    inner join {{ ref('stg_embedded_movies') }} m
        on w.dlt_movie_id = m.dlt_movie_id
    where nullif(trim(w.writer_name), '') is not null
),

dedup as (
    select
        movie_id,
        dlt_movie_id,
        writer_name,
        min(writer_ordinal) as writer_ordinal
    from base
    group by 1, 2, 3
)

select
    movie_id,
    dlt_movie_id,
    writer_name,
    writer_ordinal
from dedup
