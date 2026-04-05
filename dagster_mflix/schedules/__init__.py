from dagster import ScheduleDefinition
from ..jobs import movies_job


movies_schedule = ScheduleDefinition(
    job=movies_job,
    cron_schedule="0/5 * * * *", # Run every 5 minutes
)