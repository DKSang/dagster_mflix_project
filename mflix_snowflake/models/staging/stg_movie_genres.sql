with source as (
    select *
    from {{ source('raw', 'embedded_movies__genres') }}
)

select
    _dlt_parent_id as movie_dlt_id,
    value as genre_name,
    _dlt_list_idx as genre_idx,
    _dlt_id as genre_dlt_id,
    source.* exclude (_dlt_parent_id, value, _dlt_list_idx, _dlt_id)
from source