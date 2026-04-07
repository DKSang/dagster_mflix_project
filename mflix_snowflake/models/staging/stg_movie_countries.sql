-- depends_on: {{ source('dagster_quality', 'raw_quality_gate') }}

with source as (
    select *
    from {{ source('raw', 'embedded_movies__countries') }}
)

select
    _dlt_parent_id as dlt_movie_id,
    value as country_name,
    _dlt_list_idx as country_ordinal
from source
