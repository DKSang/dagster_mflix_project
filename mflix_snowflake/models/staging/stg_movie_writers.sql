with source as (
    select *
    from {{ source('raw', 'embedded_movies__writers') }}
)

select
    _dlt_parent_id as movie_dlt_id,
    value as writer_name,
    _dlt_list_idx as writer_idx,
    _dlt_id as writer_dlt_id,
    source.* exclude (_dlt_parent_id, value, _dlt_list_idx, _dlt_id)
from source
