from apscheduler.schedulers.background import BackgroundScheduler
from .databaseUpdates import DatabaseUpdater

def start():
    scheduler = BackgroundScheduler()
    db = DatabaseUpdater()
    
    scheduler.add_job(db.setApiIdDictionary, 'interval', minutes=10)
    scheduler.add_job(db.populateAllFPLPlayerStatsByGameweek, 'interval', minutes=60)
    scheduler.start()
