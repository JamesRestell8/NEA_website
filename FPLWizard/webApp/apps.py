from django.apps import AppConfig
import pause

class WebappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webApp'


    # THIS FUNCTION WILL BE RUN TWICE UNLESS YOU USE THE --noreload OPTION IN THE TERMINAL
    def ready(self):
        # imports have to be within the ready function
        from apscheduler.schedulers.background import BackgroundScheduler
        from .databaseUpdates import DatabaseUpdater
        from datetime import datetime

        scheduler = BackgroundScheduler(daemon=True)
        db = DatabaseUpdater()

        # DatabaseUpdater function that runs all the required functions in order
        scheduler.add_job(db.tasksInOrder, 'interval', minutes=30, next_run_time=datetime.now())
        scheduler.start()