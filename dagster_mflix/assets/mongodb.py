from dagster import AssetExecutionContext, AssetKey
from dagster_embedded_elt.dlt import DagsterDltResource, dlt_assets
from dagster_dlt import DagsterDltTranslator

import dlt
from ..mongodb import mongodb


class RawPrefixDltTranslator(DagsterDltTranslator):
    def get_asset_key(self, data):
        base_key = super().get_asset_key(data)
        return AssetKey(["raw", *base_key.path])


mflix = mongodb(
    database='sample_mflix',
    incremental=dlt.sources.incremental("_id"),
    write_disposition="merge",
).with_resources(
    "comments",
    "embedded_movies"
)


@dlt_assets(
    dlt_source=mflix,
    dlt_pipeline=dlt.pipeline(
        pipeline_name="local_mongo",
        destination='snowflake',
        dataset_name="mflix",
    ),
    name="mongodb",
    group_name="mongodb",
    dagster_dlt_translator=RawPrefixDltTranslator(),
)
def dlt_asset_factory(context: AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)