from dagster import ScheduleDefinition
from ..jobs import movies_job, quality_job


movies_schedule = ScheduleDefinition(
	job=movies_job,
	cron_schedule="0/5 * * * *", # Run every 5 minutes
)


quality_schedule = ScheduleDefinition(
	job=quality_job,
	cron_schedule="15 * * * *", # Run hourly at minute 15
)