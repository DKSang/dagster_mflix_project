with base as (
    select distinct
        director_name
    from {{ ref('stg_movie_directors') }}
    where director_name is not null
)

select
    row_number() over (order by director_name) as director_id,
    director_name
from base