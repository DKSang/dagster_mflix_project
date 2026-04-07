from pathlib import Path

import pandas as pd
from dagster import asset
from sklearn.linear_model import LinearRegression


DATA_DIR = Path("data")
TOP_MOVIES_CSV = DATA_DIR / "top_movies_by_month.csv"
ENGAGEMENT_CSV = DATA_DIR / "movie_engagement.csv"


def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _read_csv_or_empty(path: Path, columns: list[str]) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=columns)
    return pd.read_csv(path)


@asset(
    deps=["top_movies_by_month"],
)
def ad_hoc_genre_interest_report() -> None:
    """Ad-hoc report: genre-level popularity and quality snapshot."""
    _ensure_data_dir()
    df = _read_csv_or_empty(
        TOP_MOVIES_CSV,
        ["TITLE", "IMDB__RATING", "IMDB__VOTES", "GENRES", "partition_date"],
    )

    output_path = DATA_DIR / "ad_hoc_genre_interest_report.csv"
    if df.empty:
        pd.DataFrame(
            columns=["genre", "movie_count", "avg_rating", "avg_votes"]
        ).to_csv(output_path, index=False)
        return

    report = (
        df.groupby("GENRES", dropna=False)
        .agg(
            movie_count=("TITLE", "count"),
            avg_rating=("IMDB__RATING", "mean"),
            avg_votes=("IMDB__VOTES", "mean"),
        )
        .reset_index()
        .rename(columns={"GENRES": "genre"})
        .sort_values(by=["movie_count", "avg_rating"], ascending=[False, False])
    )
    report.to_csv(output_path, index=False)


@asset(
    deps=["user_engagement", "top_movies_by_month"],
)
def bi_kpi_snapshot() -> None:
    """BI snapshot: one-row KPI extract for quick dashboard consumption."""
    _ensure_data_dir()
    engagement = _read_csv_or_empty(
        ENGAGEMENT_CSV,
        ["TITLE", "YEAR_RELEASED", "NUMBER_OF_COMMENTS"],
    )
    top_movies = _read_csv_or_empty(
        TOP_MOVIES_CSV,
        ["TITLE", "IMDB__RATING", "GENRES", "partition_date"],
    )

    if engagement.empty:
        total_movies = 0
        total_comments = 0
        top_movie_title = None
        top_movie_comments = 0
    else:
        total_movies = int(engagement["TITLE"].nunique())
        total_comments = int(engagement["NUMBER_OF_COMMENTS"].sum())
        top_row = engagement.sort_values("NUMBER_OF_COMMENTS", ascending=False).iloc[0]
        top_movie_title = top_row["TITLE"]
        top_movie_comments = int(top_row["NUMBER_OF_COMMENTS"])

    if top_movies.empty:
        latest_partition = None
        genres_covered = 0
        latest_partition_avg_rating = None
    else:
        latest_partition = str(top_movies["partition_date"].max())
        genres_covered = int(top_movies["GENRES"].nunique())
        latest_slice = top_movies[top_movies["partition_date"] == latest_partition]
        latest_partition_avg_rating = float(latest_slice["IMDB__RATING"].mean())

    pd.DataFrame(
        [
            {
                "total_movies_tracked": total_movies,
                "total_comments": total_comments,
                "top_movie_title": top_movie_title,
                "top_movie_comments": top_movie_comments,
                "latest_partition": latest_partition,
                "genres_covered": genres_covered,
                "latest_partition_avg_rating": latest_partition_avg_rating,
            }
        ]
    ).to_csv(DATA_DIR / "bi_kpi_snapshot.csv", index=False)


@asset(
    deps=["top_movies_by_month"],
)
def ml_monthly_rating_forecast() -> None:
    """Simple ML baseline: forecast next 3 monthly average ratings."""
    _ensure_data_dir()
    df = _read_csv_or_empty(
        TOP_MOVIES_CSV,
        ["IMDB__RATING", "partition_date"],
    )
    output_path = DATA_DIR / "ml_monthly_rating_forecast.csv"

    if df.empty or df["partition_date"].dropna().empty:
        pd.DataFrame(
            columns=["month_start", "predicted_avg_rating", "model", "training_points"]
        ).to_csv(output_path, index=False)
        return

    monthly = (
        df.assign(partition_date=pd.to_datetime(df["partition_date"]))
        .groupby("partition_date", as_index=False)
        .agg(avg_rating=("IMDB__RATING", "mean"))
        .sort_values("partition_date")
        .reset_index(drop=True)
    )

    monthly["month_index"] = monthly.index.astype(float)
    x_train = monthly[["month_index"]].values
    y_train = monthly["avg_rating"].values
    training_points = int(len(monthly))

    if training_points >= 2:
        model = LinearRegression()
        model.fit(x_train, y_train)

        future_indices = pd.DataFrame(
            {"month_index": [training_points, training_points + 1, training_points + 2]}
        )
        predictions = model.predict(future_indices[["month_index"]].values)
        future_dates = pd.date_range(
            monthly["partition_date"].max() + pd.offsets.MonthBegin(1),
            periods=3,
            freq="MS",
        )
        forecast = pd.DataFrame(
            {
                "month_start": future_dates.astype(str),
                "predicted_avg_rating": predictions,
                "model": "linear_regression",
                "training_points": training_points,
            }
        )
    else:
        baseline = float(monthly["avg_rating"].iloc[0])
        future_dates = pd.date_range(
            monthly["partition_date"].max() + pd.offsets.MonthBegin(1),
            periods=3,
            freq="MS",
        )
        forecast = pd.DataFrame(
            {
                "month_start": future_dates.astype(str),
                "predicted_avg_rating": [baseline, baseline, baseline],
                "model": "naive_baseline",
                "training_points": training_points,
            }
        )

    forecast.to_csv(output_path, index=False)
