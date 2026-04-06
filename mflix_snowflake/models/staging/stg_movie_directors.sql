with source as (
    select *
    from {{ source('raw', 'embedded_movies__directors') }}
)

select
    _dlt_parent_id as movie_dlt_id,
    value as director_name,
    _dlt_list_idx as director_idx,
    _dlt_id as director_dlt_id,
    source.* exclude (_dlt_parent_id, value, _dlt_list_idx, _dlt_id)
from source
