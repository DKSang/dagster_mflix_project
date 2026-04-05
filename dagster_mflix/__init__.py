from dagster import Definitions, load_assets_from_modules,EnvVar
from .assets import mongodb,movies
from .resources import snowflake_resource,dlt_resource
from .schedules import movies_schedule
from .jobs import movies_job

mongodb_assets = load_assets_from_modules([mongodb])
movies_assets = load_assets_from_modules([movies],group_name="movies")

defs = Definitions(
    assets=[*mongodb_assets,*movies_assets],
    resources={
        "dlt": dlt_resource,
        "snowflake": snowflake_resource
    },
    jobs=[movies_job],
    schedules=[movies_schedule]
)