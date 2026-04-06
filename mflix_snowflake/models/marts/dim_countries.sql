with base as (
    select distinct
        country_name
    from {{ ref('stg_movie_countries') }}
    where country_name is not null
)

select
    row_number() over (order by country_name) as country_id,
    country_name
from base
