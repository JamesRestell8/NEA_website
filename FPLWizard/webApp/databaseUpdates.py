from datetime import datetime
import requests
from requests.exceptions import ConnectionError
import pandas as pd
import time
import json

from .models import *
from FPLWizard.settings import BASE_DIR
from .fplStatsClass import FPLStats
from .understatClass import UnderstatStats
from .team import TeamUpdater
from .fixture import FixtureUpdater
from .fplGeneralInfo import PlayerGeneralInfoUpdater

# removes an error that is raised when modifying data in a pandas DataFrame
pd.options.mode.chained_assignment = None

class DatabaseUpdater():
    def __init__(self):
        self.time = datetime.now()

    def setApiIdDictionary(self):
        # this function should only run when the table is empty (on initialisation)
        if len(APIIDDictionary.objects.all()) < 10:
            # read the id dictionary from Vaastav into a dataframe to be stored in the database
            table = pd.read_csv(f"{BASE_DIR}/webApp/id_dict.csv")
            fplIDs = table['FPL_ID']
            understatIDs = table['Understat_ID']
            fplNames = table['FPL_Name']
            understatNames = table['Understat_Name']
            # for every entry in the .csv file, save the data into the database as a row
            for i in range(len(fplIDs)):
                row = APIIDDictionary(playerID=i+1, fplID=fplIDs[i], understatID=understatIDs[i],
                                    fplName=fplNames[i], understatName=understatNames[i])
                row.save()


    def getFPLPlayerStatsByGameweek(self, FPLplayerID: int):
        x = FPLStats(FPLplayerID)
        x.populateDatabase()
    
    # NOTE: the FPL API will return all player gameweeks, even if they didn't feature. Understat only keeps records of player gameweeks where the player featured.
    def populateAllFPLPlayerStatsByGameweek(self):
        # time delay to allow for admin tasks in terminal
        time.sleep(5)

        # get all players
        ids = APIIDDictionary.objects.all()
        # for each player, get all their gameweeks and add them to the FPLGameweek table in DB
        for entry in ids:
            self.getFPLPlayerStatsByGameweek(entry.fplID)

    def getUnderstatPlayerStatsByGameweek(self, understatID: int):
        x = UnderstatStats(understatID)
        x.populateDatabase()

    def populateAllUnderstatPlayerStatsByGameweek(self):
        # time delay to allow for admin tasks in terminal
        time.sleep(5)
        ids = APIIDDictionary.objects.all()

        for entry in ids:
            self.getUnderstatPlayerStatsByGameweek(entry.understatID)

    def updateTeamTable(self):
        updater = TeamUpdater()
        updater.populateDatabase()

    def updateFixtureTable(self):
        updater = FixtureUpdater()
        updater.populateDatabase()

    def updateGeneralInfo(self):
        updater = PlayerGeneralInfoUpdater()
        updater.populateDatabase()

    def tasksInOrder(self):
        # time delay to allow time to perform admin tasks in the terminal before print statements
        time.sleep(2)
        masterStart = time.time()
        # executes in less than 20 seconds
        self.setApiIdDictionary()
        print("ID dictionary done", end='\n')
        self.updateFixtureTable()
        print("Fixtures done", end='\n')
        self.updateTeamTable()
        print("teams updated", end="\n")
        # ~ 8 mins
        start = time.time()
        self.populateAllFPLPlayerStatsByGameweek()
        end = time.time()
        print(f"FPL database done in {end - start} seconds")
        # ~ 10 mins
        start = time.time()
        self.populateAllUnderstatPlayerStatsByGameweek()
        end = time.time()
        print(f"Understat database done in {end - start} seconds")
        print("general info...")
        start = time.time()
        self.updateGeneralInfo()
        end = time.time()
        masterEnd = time.time()
        print(f"General info updated in {end-start} seconds", end='\n')
        print(f"All database jobs done in {masterEnd-masterStart} seconds")
