with movie_base as (
	select
		movie_id,
		dlt_movie_id,
		title,
		year,
		released,
		runtime,
		imdb_rating,
		imdb_votes
	from {{ ref('stg_embedded_movies') }}
),

movies as (
	select
		movie_id,
		dlt_movie_id,
		title,
		year,
		released,
		runtime,
		imdb_rating,
		imdb_votes
	from movie_base
	qualify row_number() over (
		partition by movie_id
		order by released desc nulls last, dlt_movie_id desc
	) = 1
),

genres as (
	{{ aggregate_primary_and_list('stg_movie_genres', 'dlt_movie_id', 'genre_name', 'genre_ordinal', 'primary_genre_name', 'genre_names') }}
),

countries as (
	{{ aggregate_primary_and_list('stg_movie_countries', 'dlt_movie_id', 'country_name', 'country_ordinal', 'primary_country_name', 'country_names') }}
),

languages as (
	{{ aggregate_primary_and_list('stg_movie_languages', 'dlt_movie_id', 'language_name', 'language_ordinal', 'primary_language_name', 'language_names') }}
),

directors as (
	{{ aggregate_primary_and_list('stg_movie_directors', 'dlt_movie_id', 'director_name', 'director_ordinal', 'primary_director_name', 'director_names') }}
),

writers as (
	{{ aggregate_primary_and_list('stg_movie_writers', 'dlt_movie_id', 'writer_name', 'writer_ordinal', 'primary_writer_name', 'writer_names') }}
),

cast_members as (
	{{ aggregate_list_only('stg_movie_cast', 'dlt_movie_id', 'cast_name', 'cast_names') }}
)

select
	m.movie_id,
	m.dlt_movie_id,
	m.title,
	m.year,
	m.released,
	m.runtime,
	m.imdb_rating,
	m.imdb_votes,
	g.primary_genre_name,
	g.genre_names,
	c.primary_country_name,
	c.country_names,
	l.primary_language_name,
	l.language_names,
	d.primary_director_name,
	d.director_names,
	w.primary_writer_name,
	w.writer_names,
	cm.cast_names
from movies m
left join genres g
	on m.dlt_movie_id = g.dlt_movie_id
left join countries c
	on m.dlt_movie_id = c.dlt_movie_id
left join languages l
	on m.dlt_movie_id = l.dlt_movie_id
left join directors d
	on m.dlt_movie_id = d.dlt_movie_id
left join writers w
	on m.dlt_movie_id = w.dlt_movie_id
left join cast_members cm
	on m.dlt_movie_id = cm.dlt_movie_id
