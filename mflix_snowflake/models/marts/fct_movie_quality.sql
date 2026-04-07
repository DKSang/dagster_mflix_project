with movie_profile as (
    select
        movie_id,
        title,
        year,
        runtime,
        imdb_rating,
        imdb_votes,
        primary_genre_name
    from {{ ref('int_movie_flattened') }}
    where movie_id is not null
),

quality as (
    select
        m.movie_id,
        m.title,
        g.genre_id as primary_genre_id,
        m.year,
        m.runtime,
        m.imdb_rating,
        m.imdb_votes,
        case
            when m.imdb_rating >= 8 then 'Excellent'
            when m.imdb_rating >= 6 then 'Good'
            when m.imdb_rating >= 4 then 'Average'
            else 'Low'
        end as rating_bucket,
        -- Weighted score to reduce bias from low vote counts.
        round((coalesce(m.imdb_rating, 0) * ln(1 + coalesce(m.imdb_votes, 0))), 4) as weighted_quality_score
    from movie_profile m
    left join {{ ref('dim_genres') }} g
        on m.primary_genre_name = g.genre_name
)

select
    movie_id,
    title,
    primary_genre_id,
    year,
    runtime,
    imdb_rating,
    imdb_votes,
    rating_bucket,
    weighted_quality_score
from quality