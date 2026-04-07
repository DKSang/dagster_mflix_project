with base as (
    select distinct
        country_name
    from {{ ref('int_movie_countries_bridge') }}
    where country_name is not null
)

select
    row_number() over (order by country_name) as country_key,
    country_name,
    upper(replace(replace(country_name, ' ', '_'), '-', '_')) as country_code
from base