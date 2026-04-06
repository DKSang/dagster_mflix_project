with base as (
    select distinct
        cast_name
    from {{ ref('stg_movie_cast') }}
    where cast_name is not null
)

select
    row_number() over (order by cast_name) as cast_id,
    cast_name
from base