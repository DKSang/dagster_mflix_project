with source as (
    select *
    from {{ source('raw', 'embedded_movies__cast') }}
)

select
    _dlt_parent_id as movie_dlt_id,
    value as cast_name,
    _dlt_list_idx as cast_idx,
    _dlt_id as cast_dlt_id,
    source.* exclude (_dlt_parent_id, value, _dlt_list_idx, _dlt_id)
from source
