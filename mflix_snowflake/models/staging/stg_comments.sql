
with source as (
    select *
    from {{ source('raw', 'comments') }}
)

select
    _id as comment_id,
    movie_id,
    text as comment_text,
    date as comment_date,
    name as commenter_name,
    email as commenter_email,
    source.* exclude (_id, movie_id, text, date, name, email)
from source