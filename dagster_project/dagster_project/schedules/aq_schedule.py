from dagster import ScheduleDefinition
from dagster_project.jobs.aq_job import aq_job

aq_schedule = ScheduleDefinition(
    job=aq_job,
    cron_schedule="0 8 * * *",  # 8AM daily, UTC Time
    name="daily_aq_schedule"
)
