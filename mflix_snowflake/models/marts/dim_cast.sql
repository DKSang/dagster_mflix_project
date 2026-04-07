with base as (
    select distinct
        cast_name
    from {{ ref('int_movie_cast_bridge') }}
    where cast_name is not null
)

select
    row_number() over (order by cast_name) as cast_id,
    cast_name
from base