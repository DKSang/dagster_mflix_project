with base as (
    select distinct
        writer_name
    from {{ ref('stg_movie_writers') }}
    where writer_name is not null
)

select
    row_number() over (order by writer_name) as writer_id,
    writer_name
from base