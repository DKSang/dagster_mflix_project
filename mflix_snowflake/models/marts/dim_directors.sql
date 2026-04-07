with base as (
    select
        director_name
    from {{ ref('int_movie_directors_bridge') }}
    where director_name is not null

    union all

    select 'Unknown' as director_name
),

dedup as (
    select distinct
        director_name
    from base
)

select
    row_number() over (order by director_name) as director_id,
    director_name
from dedup