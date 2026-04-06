from pathlib import Path

from dagster import EnvVar
from dagster_embedded_elt.dlt import DagsterDltResource
from dagster_snowflake import SnowflakeResource
from dagster_dbt import DbtCliResource


REPO_ROOT = Path(__file__).resolve().parents[2]

snowflake_resource = SnowflakeResource(
    account=EnvVar("SNOWFLAKE_ACCOUNT"),  # required
    user=EnvVar("SNOWFLAKE_USER"),  # required
    password=EnvVar("SNOWFLAKE_PASSWORD"),  # password or private key required
    warehouse="dagster_wh",
    database="dagster_db",
    schema="mflix",
    role="dagster_role",
)

dlt_resource = DagsterDltResource()
dbt_resource = DbtCliResource(
    project_dir="mflix_snowflake",
    profiles_dir="/home/dksan/.dbt",
    dbt_executable=str(REPO_ROOT / ".venv" / "bin" / "dbt"),
)