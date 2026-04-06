from dagster import AssetSelection, define_asset_job
from ..partitions import monthly_partition


movies_job = define_asset_job(
	name="movies_job",
	partitions_def=monthly_partition,
	selection=AssetSelection.all() - AssetSelection.groups("mongodb") # Use groups instead of assets
)
