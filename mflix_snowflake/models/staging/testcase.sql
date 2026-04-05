with source as
(
    select
        *
    from {{ source('raw', 'COMMENTS') }}
)
select
    *
from source