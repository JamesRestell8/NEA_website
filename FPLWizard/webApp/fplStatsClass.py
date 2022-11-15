import time
import requests
from requests import ConnectionError
import pandas as pd

from .models import FPLAPIStatsGameweek, APIIDDictionary

class fplStats():
    def __init__(self, fplID: int):
        self.fplID = fplID
        
        # these should all be methods that access the database rather than their own attributes. (applies to both getters and setters)
        self.fplPlayerName = ""
        self.minutes = 0
        self.goals = 0
        self.assists = 0
        self.goalsConceded = 0
        self.cleanSheets = 0
        self.totalPoints = 0
        self.teamID = 0
        self.position = 0
        self.cost = 0
        self.threat = 0
        self.influence = 0
        self.creativity = 0
        self.pointsPerGame = 0

    # INSERT GETTERS AND SETTERS FOR ALL ATTRIBUTES HERE


    def populateAllGameweeks(self):
        url = f"https://fantasy.premierleague.com/api/element-summary/{self.fplID}/"

        # code to request API over 15 second period in case of connection delays
        found = False
        i = 0
        while i < 15 and not found:
            try:
                r = requests.get(url)
                found = True
            except ConnectionError:
                time.sleep(1)
                i += 1

        # only add to database if API request was successful
        if found:
            r = r.json()
            stats = pd.json_normalize(r['history'])
            stats = stats[['element', 'fixture',
            'total_points','round', 'minutes', 'goals_scored', 'assists', 
            'clean_sheets', 'goals_conceded', 'influence', 
            'creativity', 'threat', 'value']]

            # TEAM AND POSITION NEED TO BE RETREIVED FROM GENERAL INFORMATION (NEW CLASS AND DATABASE TABLE NEEDED!)
            for i in range(len(stats['element'])):
                row = FPLAPIStatsGameweek(
                    fpl_id = self.fplID,
                    fpl_fixtureID = stats['fixture'][i],
                    fpl_gameweekNumber = stats['round'][i],
                    fpl_player_name = APIIDDictionary.objects.get(fplID=self.fplID).fplName,
                    fpl_minutes = stats['minutes'][i],
                    fpl_assists = stats['assists'][i],
                    fpl_goals = stats['goals_scored'][i],
                    fpl_clean_sheets = stats['clean_sheets'][i],
                    fpl_goals_conceded = stats['goals_conceded'][i],
                    fpl_total_points = stats['total_points'][i],
                    fpl_team = 0,
                    fpl_position = 0,
                    fpl_cost = stats['value'][i],
                    fpl_threat = stats['threat'][i],
                    fpl_influence = stats['influence'][i],
                    fpl_creativity = stats['creativity'][i]
                )
                row.save()
