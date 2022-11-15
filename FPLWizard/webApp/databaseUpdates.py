from datetime import datetime
import requests
from requests.exceptions import ConnectionError
import pandas as pd
import time
import json

from .models import *

# removes an error that is raised when modifying data in a pandas DataFrame
pd.options.mode.chained_assignment = None

class DatabaseUpdater():
    # for the convenience of the user, the database should update
    # every day at midnight, so that the most recent fixture results
    # can be added before changes need to be made the next day
    def __init__(self, firstUpdate: bool):
        self.firstUpdate = firstUpdate
        self.time = datetime.datetime()
        self.fplURL = "https://fantasy.premierleague.com/api/bootstrap-static/"
        if len(APIIDDictionary.objects.all()) == 0:
            self.idSet = False
        else:
            self.idSet = True
    
    # need to determine which tables need to be updated live,
    # and which tables can just be left for the whole season
    # need methods to update and populatre all of the fields in the
    # database daily.

    def setApiIdDictionary(self):
        table = pd.read_csv("id_dict.csv")

        for row in table.iterrows():
            # add row to database in correct order, may need to test how iterrows works in empty file
            pass


    def updateFPLTable(self, gameweek: int):
        # THIS IS FOR AGGREGATE STATS, NEED TO MAKE ONE FOR SPECIFIC GAMEWEEKS PER PLAYER
        found = False
        i = 0
        while i < 30 and not found:
            try:
                r = requests.get(self.fplURL)
                found = True
            except ConnectionError:
                time.sleep(1)
                i += 1
        jsonData = r.json()

        stats = pd.DataFrame(jsonData['elements'])
        statsFiltered = stats[['id', 'first_name', 'second_name', 'minutes',
        'assists', 'goals', 'clean_sheets', 'goals_conceded', 'total_points',
        'team', 'element_type', 'now_cost', 'threat', 'influence', 'creativity',
        'points_per_game']]

        # change first name and last name columns to full name:
        statsFiltered['full_name'] = statsFiltered['first_name'] + " " + statsFiltered['second_name']
        del statsFiltered['first_name']
        del statsFiltered['second_name']

        # move full name column to the front
        cols = statsFiltered.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        statsFiltered = statsFiltered[cols]

        # statsFiltered now contains a dataframe of all current player stats

