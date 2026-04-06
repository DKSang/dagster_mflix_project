from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets

DBT_MANIFEST = "mflix_snowflake/target/manifest.json"
DBT_OP_TAGS = {"dagster/kind/dbt": "", "dagster/kind/snowflake": ""}


@dbt_assets(
    manifest=DBT_MANIFEST,
    select="staging.*",
    op_tags=DBT_OP_TAGS,
)
def dbt_staging(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
