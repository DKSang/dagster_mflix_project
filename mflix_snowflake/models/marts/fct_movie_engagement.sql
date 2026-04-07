select
  c.movie_id,
  m.title,
  g.genre_id as primary_genre_id,
  co.country_key as primary_country_id,
  l.language_id as primary_language_id,
  d.director_id as primary_director_id,
  w.writer_id as primary_writer_id,
  count(*) as number_of_comments,
  min(c.comment_date) as first_comment_date,
  max(c.comment_date) as last_comment_date
from {{ ref('stg_comments') }} c
inner join {{ ref('int_movie_flattened') }} m
  on c.movie_id = m.movie_id
left join {{ ref('dim_genres') }} g
  on m.primary_genre_name = g.genre_name
left join {{ ref('dim_country') }} co
  on m.primary_country_name = co.country_name
left join {{ ref('dim_languages') }} l
  on coalesce(m.primary_language_name, 'Unknown') = l.language_name
left join {{ ref('dim_directors') }} d
  on coalesce(m.primary_director_name, 'Unknown') = d.director_name
left join {{ ref('dim_writers') }} w
  on coalesce(m.primary_writer_name, 'Unknown') = w.writer_name
group by 1, 2, 3, 4, 5, 6, 7
