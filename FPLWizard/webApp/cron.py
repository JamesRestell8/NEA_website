""" 
This file is responsible for all background tasks relating to database maintenance
in the project. This allows webpages to render normally whilst database related
tasks run in the background.
"""

from django_cron import CronJobBase, Schedule
from .models import *
from .databaseUpdates import DatabaseUpdater

class DBCronJobs(CronJobBase):
    RUN_EVERY_MINS = 1
    RETRY_AFTER_FAILURE_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = "news.db_cron_jobS"

    def do(self):
        db = DatabaseUpdater()
        db.setApiIdDictionary()
        db.populateAllFPLPlayerStatsByGameweek()