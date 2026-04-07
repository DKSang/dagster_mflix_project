from dagster import AssetSelection, define_asset_job
from ..partitions import monthly_partition


movies_job = define_asset_job(
	name="movies_job",
	partitions_def=monthly_partition,
	selection=AssetSelection.all() - AssetSelection.groups("mongodb") # Use groups instead of assets
)


transform_job = define_asset_job(
	name="transform_job",
	partitions_def=monthly_partition,
	selection=AssetSelection.groups("staging", "intermediate", "marts")
)


quality_job = define_asset_job(
	name="quality_job",
	partitions_def=monthly_partition,
	selection=AssetSelection.groups("quality")
)


ad_hoc_job = define_asset_job(
	name="ad_hoc_job",
	selection=AssetSelection.assets("ad_hoc_genre_interest_report")
)


bi_job = define_asset_job(
	name="bi_job",
	selection=AssetSelection.assets("bi_kpi_snapshot")
)


ml_job = define_asset_job(
	name="ml_job",
	selection=AssetSelection.assets("ml_monthly_rating_forecast")
)
