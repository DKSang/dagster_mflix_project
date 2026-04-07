# BI/DA/DS Requirements for 3 Models

Status: approved-for-implementation
Date: 2026-04-06

## Scope

Tai lieu nay tong hop day du yeu cau tu BI, DA, DS cho 3 model muc tieu de team trien khai trong Epic 2.

3 model trong pham vi:
1. `int_movie_flattened` (intermediate)
2. `fct_movie_consumption_daily` (mart core fact)
3. `agg_movie_country_daily` (mart geo aggregate)

Quyet dinh da chot:
- Grain fact chinh: movie-day (`movie_id` + `date_key`)
- Geo khong nhan vao key fact chinh, duoc tach qua aggregate rieng

## Stakeholder Requirements

### BI Requirements

Muc tieu BI:
- Dashboard top movies theo thang, quoc gia, the loai
- Theo doi xu huong watch-time, views, completion rate theo ngay

Yeu cau chi tiet:
1. Co metric on dinh cho ranking:
   - `total_views`
   - `total_watch_time`
   - `completion_rate`
2. Co kha nang slice theo:
   - thoi gian (day/month)
   - quoc gia
   - the loai
3. Ranking deterministic khi dong diem:
   - tie-break theo `movie_id` tang dan
4. Schema output on dinh cho dashboard:
   - khong doi ten cot tuy y
   - moi thay doi cot phai co changelog

### DA Requirements

Muc tieu DA:
- Truy van ad-hoc nhanh
- Drill-down month -> day -> movie

Yeu cau chi tiet:
1. Grain ro rang va documented:
   - Fact core: 1 dong / `movie_id` / `date_key`
2. Join de dang voi dimensions:
   - movie
   - date
   - country (qua aggregate geo)
3. Co data dictionary toi thieu:
   - dinh nghia metric
   - cong thuc tinh
   - handling null/zero
4. Truy vet metric duoc:
   - metric mart map ve cot staging nguon

### DS Requirements

Muc tieu DS:
- Trich feature theo cua so thoi gian de phuc vu mo hinh

Yeu cau chi tiet:
1. Ho tro feature rolling:
   - `views_7d`, `views_28d`
   - `watch_time_7d`
   - `completion_rate_28d`
2. Dinh danh movie on dinh:
   - `movie_id` khong null
   - khong duplicate theo grain
3. Giam nhieu du lieu:
   - fact core giu tong hop movie-day
   - geo dung aggregate khi can huan luyen theo thi truong
4. Tinh tai lap duoc:
   - cung input -> cung output (deterministic transform)

## Model Contracts

## 1) int_movie_flattened

Model path:
- `mflix_snowflake/models/intermediate/int_movie_flattened.sql`

Muc tieu:
- Chuan hoa thong tin movie tu staging thanh 1 bang intermediate de nuoi dims/facts

Input:
- `stg_embedded_movies`
- `stg_movie_genres`
- `stg_movie_countries`
- `stg_movie_languages`
- `stg_movie_directors`
- `stg_movie_writers`
- `stg_movie_cast`

Output columns bat buoc:
- `movie_id`
- `movie_dlt_id`
- `title`
- `year`
- `released`
- `runtime`
- `imdb_rating`
- `imdb_votes`
- `primary_genre_name`
- `genre_names`
- `primary_country_name`
- `country_names`
- `primary_language_name`
- `language_names`
- `primary_director_name`
- `director_names`
- `primary_writer_name`
- `writer_names`
- `cast_names`

Business rules:
1. 1 dong / movie (`movie_id`) sau khi aggregate nested fields
2. Gia tri primary lay theo ordinal nho nhat
3. Danh sach names dung `listagg(distinct ..., ', ')` co order on dinh

Quality rules:
1. `movie_id` not null
2. `movie_id` unique
3. Text values trim truoc khi aggregate

## 2) fct_movie_consumption_daily

Model path de tao moi:
- `mflix_snowflake/models/marts/fct_movie_consumption_daily.sql`

Muc tieu:
- Fact core cho BI/DA/DS o grain movie-day

Grain:
- 1 dong / `movie_id` / `date_key`

Output columns bat buoc:
- `movie_id`
- `date_key`
- `total_views`
- `total_watch_time`
- `unique_viewers`
- `completion_rate`
- `avg_watch_time`
- `first_event_ts`
- `last_event_ts`

Business rules:
1. `completion_rate` = completed_views / total_views (null-safe)
2. `avg_watch_time` = total_watch_time / total_views (null-safe)
3. Khong dua country vao key fact core

Quality rules:
1. unique composite key (`movie_id`, `date_key`)
2. not null key columns
3. metric count/time non-negative
4. lineage map moi metric ve cot staging nguon

## 3) agg_movie_country_daily

Model path de tao moi:
- `mflix_snowflake/models/marts/agg_movie_country_daily.sql`

Muc tieu:
- Aggregate geo de BI slice theo country ma khong lam phinh fact core

Grain:
- 1 dong / `movie_id` / `date_key` / `country_key`

Output columns bat buoc:
- `movie_id`
- `date_key`
- `country_key`
- `country_code`
- `country_name`
- `total_views`
- `total_watch_time`
- `unique_viewers`

Business rules:
1. Metric geo aggregate phai co logic nhat quan voi fact core
2. Join voi dim_country thong qua `country_key`
3. Country tie-break/order deterministic

Quality rules:
1. unique composite key (`movie_id`, `date_key`, `country_key`)
2. relationships voi `dim_country`
3. `country_code` theo accepted_values (ISO policy cua du an)
4. Reconciliation voi fact core theo movie-day trong nguong cho phep

## Traceability Matrix (BI/DA/DS -> Model)

1. BI-01 Top movies theo thang/quoc gia/the loai
- Fact/agg: `fct_movie_consumption_daily`, `agg_movie_country_daily`
- Dim: `dim_movies`, `dim_genres`, `dim_date`, `dim_country`

2. BI-02 Theo doi completion_rate va watch_time theo ngay
- Fact: `fct_movie_consumption_daily`

3. DA-01 Drill-down month -> day -> movie
- Fact: `fct_movie_consumption_daily`
- Aggregate bo sung: `agg_movie_country_daily`

4. DS-01 Feature rolling 7/28 ngay
- Nguon feature: `fct_movie_consumption_daily`
- Geo feature (tuy chon): `agg_movie_country_daily`

## Implementation Tasks (Actionable)

1. Chuan hoa intermediate
- Cap nhat `int_movie_flattened.sql` theo contract tren

2. Tao fact core moi
- Tao `fct_movie_consumption_daily.sql`
- Khai bao grain, metrics, null-safe formulas

3. Tao geo aggregate moi
- Tao `agg_movie_country_daily.sql`
- Join voi `dim_country` va ap dung reconciliation check

4. Cap nhat schema va tests
- Cap nhat `mflix_snowflake/models/marts/schema.yml`
- Them tests unique/not_null/relationships/accepted_values

5. Validate bang dbt (uv-first)
- `uv run dbt build --project-dir mflix_snowflake --select int_movie_flattened fct_movie_consumption_daily agg_movie_country_daily`
- `uv run dbt test --project-dir mflix_snowflake --select fct_movie_consumption_daily agg_movie_country_daily`

## Acceptance Criteria (Given/When/Then)

1. Given du lieu staging hop le
   When chay model `int_movie_flattened`
   Then output co 1 dong moi `movie_id`
   And nested attributes duoc aggregate on dinh.

2. Given comments/events theo ngay
   When chay model `fct_movie_consumption_daily`
   Then fact co grain `movie_id` + `date_key`
   And completion_rate, avg_watch_time tinh null-safe.

3. Given du lieu country-level
   When chay model `agg_movie_country_daily`
   Then output co grain `movie_id` + `date_key` + `country_key`
   And tong metric geo co the doi soat voi fact core trong nguong chap nhan.
