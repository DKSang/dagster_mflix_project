with base as (
  select
    date_trunc('month', released) as month_start,
    movie_id,
    title,
    imdb_rating,
    imdb_votes,
    row_number() over (
      partition by date_trunc('month', released)
      order by imdb_rating desc, imdb_votes desc
    ) as rn
  from {{ ref('stg_embedded_movies') }}
  where released is not null
)

select
  month_start,
  movie_id,
  title,
  imdb_rating,
  imdb_votes
from base
where rn <= 10
