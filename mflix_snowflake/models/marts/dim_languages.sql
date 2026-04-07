with base as (
    select
        language_name
    from {{ ref('int_movie_languages_bridge') }}
    where language_name is not null

    union all

    select 'Unknown' as language_name
),

dedup as (
    select distinct
        language_name
    from base
)

select
    row_number() over (order by language_name) as language_id,
    language_name
from dedup
