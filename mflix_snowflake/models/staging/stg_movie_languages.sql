with source as (
    select *
    from {{ source('raw', 'embedded_movies__languages') }}
)

select
    _dlt_parent_id as movie_dlt_id,
    value as language_name,
    _dlt_list_idx as language_idx,
    _dlt_id as language_dlt_id,
    source.* exclude (_dlt_parent_id, value, _dlt_list_idx, _dlt_id)
from source
