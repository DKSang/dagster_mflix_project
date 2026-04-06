with movies as (
    select
        movie_id,
        _dlt_id as movie_dlt_id,
        title,
        year,
        released,
        runtime,
        imdb_rating,
        imdb_votes
    from {{ ref('stg_embedded_movies') }}
),

genres as (
    select
        movie_dlt_id,
        min_by(genre_name, genre_idx) as primary_genre_name,
        listagg(distinct genre_name, ', ') within group (order by genre_name) as genre_names
    from {{ ref('stg_movie_genres') }}
    group by 1
),

countries as (
    select
        movie_dlt_id,
        min_by(country_name, country_idx) as primary_country_name,
        listagg(distinct country_name, ', ') within group (order by country_name) as country_names
    from {{ ref('stg_movie_countries') }}
    group by 1
),

languages as (
    select
        movie_dlt_id,
        min_by(language_name, language_idx) as primary_language_name,
        listagg(distinct language_name, ', ') within group (order by language_name) as language_names
    from {{ ref('stg_movie_languages') }}
    group by 1
),

directors as (
    select
        movie_dlt_id,
        min_by(director_name, director_idx) as primary_director_name,
        listagg(distinct director_name, ', ') within group (order by director_name) as director_names
    from {{ ref('stg_movie_directors') }}
    group by 1
),

writers as (
    select
        movie_dlt_id,
        min_by(writer_name, writer_idx) as primary_writer_name,
        listagg(distinct writer_name, ', ') within group (order by writer_name) as writer_names
    from {{ ref('stg_movie_writers') }}
    group by 1
),

cast_members as (
    select
        movie_dlt_id,
        listagg(distinct cast_name, ', ') within group (order by cast_name) as cast_names
    from {{ ref('stg_movie_cast') }}
    group by 1
)

select
    m.movie_id,
    m.movie_dlt_id,
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
    on m.movie_dlt_id = g.movie_dlt_id
left join countries c
    on m.movie_dlt_id = c.movie_dlt_id
left join languages l
    on m.movie_dlt_id = l.movie_dlt_id
left join directors d
    on m.movie_dlt_id = d.movie_dlt_id
left join writers w
    on m.movie_dlt_id = w.movie_dlt_id
left join cast_members cm
    on m.movie_dlt_id = cm.movie_dlt_id