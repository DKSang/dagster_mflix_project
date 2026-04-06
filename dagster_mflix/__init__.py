from dagster import Definitions, load_assets_from_modules
from .assets import mongodb, dbt_staging, dbt_intermediate, dbt_marts
from .resources import snowflake_resource, dlt_resource, dbt_resource
from .schedules import movies_schedule
from .jobs import movies_job

mongodb_assets = load_assets_from_modules([mongodb])
dbt_staging_assets = load_assets_from_modules([dbt_staging], group_name="staging")
dbt_intermediate_assets = load_assets_from_modules([dbt_intermediate], group_name="intermediate")
dbt_marts_assets = load_assets_from_modules([dbt_marts], group_name="marts")

defs = Definitions(
    assets=[*mongodb_assets, *dbt_staging_assets, *dbt_intermediate_assets, *dbt_marts_assets],
    resources={
        "dlt": dlt_resource,
        "snowflake": snowflake_resource,
        "dbt": dbt_resource,
    },
    jobs=[movies_job],
    schedules=[movies_schedule],
)