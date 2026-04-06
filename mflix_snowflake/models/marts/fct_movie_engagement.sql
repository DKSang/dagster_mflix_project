select
  c.movie_id,
  m.title,
  g.genre_id as primary_genre_id,
  co.country_id as primary_country_id,
  l.language_id as primary_language_id,
  d.director_id as primary_director_id,
  w.writer_id as primary_writer_id,
  count(*) as number_of_comments,
  min(c.comment_date) as first_comment_date,
  max(c.comment_date) as last_comment_date
from {{ ref('stg_comments') }} c
left join {{ ref('int_movie_flattened') }} m
  on c.movie_id = m.movie_id
left join {{ ref('dim_genres') }} g
  on m.primary_genre_name = g.genre_name
left join {{ ref('dim_countries') }} co
  on m.primary_country_name = co.country_name
left join {{ ref('dim_languages') }} l
  on m.primary_language_name = l.language_name
left join {{ ref('dim_directors') }} d
  on m.primary_director_name = d.director_name
left join {{ ref('dim_writers') }} w
  on m.primary_writer_name = w.writer_name
group by 1, 2, 3, 4, 5, 6, 7
