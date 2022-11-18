from apscheduler.schedulers.background import BackgroundScheduler
from .databaseUpdates import DatabaseUpdater
from datetime import datetime

def start():
    scheduler = BackgroundScheduler(daemon=True)
    db = DatabaseUpdater()
    
    scheduler.add_job(db.tasksInOrder, 'interval', minutes=10, next_run_time=datetime.now())

    scheduler.start()
