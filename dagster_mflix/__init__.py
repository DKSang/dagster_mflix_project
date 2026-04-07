from dagster import Definitions, load_assets_from_modules
from .assets import mongodb, dbt_staging, dbt_intermediate, dbt_marts, quality, end_user
from .resources import snowflake_resource, dlt_resource, dbt_resource
from .schedules import movies_schedule, quality_schedule
from .jobs import movies_job, transform_job, quality_job, ad_hoc_job, bi_job, ml_job

mongodb_assets = load_assets_from_modules([mongodb])
dbt_staging_assets = load_assets_from_modules([dbt_staging], group_name="staging")
dbt_intermediate_assets = load_assets_from_modules([dbt_intermediate], group_name="intermediate")
dbt_marts_assets = load_assets_from_modules([dbt_marts], group_name="marts")
quality_assets = load_assets_from_modules([quality], group_name="quality")
end_user_assets = load_assets_from_modules([end_user], group_name="end_user")

defs = Definitions(
    assets=[*mongodb_assets, *dbt_staging_assets, *dbt_intermediate_assets, *dbt_marts_assets, *quality_assets, *end_user_assets],
    resources={
        "dlt": dlt_resource,
        "snowflake": snowflake_resource,
        "dbt": dbt_resource,
    },
    jobs=[movies_job, transform_job, quality_job, ad_hoc_job, bi_job, ml_job],
    schedules=[movies_schedule, quality_schedule],
)