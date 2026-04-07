-- depends_on: {{ source('dagster_quality', 'raw_quality_gate') }}

with source as (
    select *
    from {{ source('raw', 'embedded_movies__writers') }}
)

select
    _dlt_parent_id as dlt_movie_id,
    value as writer_name,
    _dlt_list_idx as writer_ordinal
from source
