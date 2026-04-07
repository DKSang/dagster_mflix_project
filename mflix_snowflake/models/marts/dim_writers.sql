with base as (
    select
        writer_name
    from {{ ref('int_movie_writers_bridge') }}
    where writer_name is not null

    union all

    select 'Unknown' as writer_name
),

dedup as (
    select distinct
        writer_name
    from base
)

select
    row_number() over (order by writer_name) as writer_id,
    writer_name
from dedup