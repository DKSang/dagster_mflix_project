with base as (
    select distinct
        language_name
    from {{ ref('stg_movie_languages') }}
    where language_name is not null
)

select
    row_number() over (order by language_name) as language_id,
    language_name
from base
