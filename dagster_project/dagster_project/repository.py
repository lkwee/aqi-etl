from dagster import Definitions
from dagster_project.jobs.aq_job import aq_job
from dagster_project.schedules.aq_schedule import daily_8am_schedule

defs = Definitions(
    jobs=[aq_job],
    schedules=[daily_aq_schedule],
)
