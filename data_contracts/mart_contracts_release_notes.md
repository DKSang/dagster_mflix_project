# MART Contract Release Notes

## Version 1.0.0 (2026-04-07)

Initial versioned release for MART data contracts.

Covered datasets:
- dim_movies
- dim_genres
- dim_country
- dim_date
- fct_movie_engagement
- fct_movie_quality
- fct_movie_consumption_daily
- agg_top_movies_by_month
- agg_top_movies_by_engagement
- agg_movie_country_daily

## Versioning Policy

- Patch increment (x.y.Z): typo or non-semantic documentation changes.
- Minor increment (x.Y.z): additive non-breaking changes, for example adding optional columns.
- Major increment (X.y.z): required for breaking changes.

Breaking changes include:
- Remove dataset from contract.
- Remove or rename column.
- Change dataset grain.
- Change primary key semantics.

Any major bump must include:
- Change rationale.
- Migration guidance for downstream dashboard/API consumers.
- Effective date for rollout.