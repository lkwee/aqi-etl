from dagster import Definitions
from .jobs.aq_job import aq_job
from .schedules.aq_schedule import aq_schedule

defs = Definitions(
    jobs=[aq_job],
    schedules=[aq_schedule]
)
