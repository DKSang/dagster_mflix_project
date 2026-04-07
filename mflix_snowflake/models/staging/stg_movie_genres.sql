-- depends_on: {{ source('dagster_quality', 'raw_quality_gate') }}

with source as (
    select *
    from {{ source('raw', 'embedded_movies__genres') }}
)
select
    _dlt_parent_id as dlt_movie_id,
    value as genre_name,
    _dlt_list_idx as genre_ordinal
from source