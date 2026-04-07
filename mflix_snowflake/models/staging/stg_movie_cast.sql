-- depends_on: {{ source('dagster_quality', 'raw_quality_gate') }}

with source as (
    select *
    from {{ source('raw', 'embedded_movies__cast') }}
)

select
    _dlt_parent_id as dlt_movie_id,
    value as cast_name,
    _dlt_list_idx as cast_ordinal
from source
