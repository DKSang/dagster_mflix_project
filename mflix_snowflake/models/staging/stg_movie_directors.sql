-- depends_on: {{ source('dagster_quality', 'raw_quality_gate') }}

with source as (
    select *
    from {{ source('raw', 'embedded_movies__directors') }}
)

select
    _dlt_parent_id as dlt_movie_id,
    value as director_name,
    _dlt_list_idx as director_ordinal
from source
