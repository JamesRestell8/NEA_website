import requests
import time
from requests import ConnectionError
import pandas as pd

from .models import FPLAPIStatsGameweek, APIIDDictionary
from .databaseManager import DatabaseManager

# This is a class that is responsible for updating a players information in the FPLAPIStatsGameweek table. 
# Every player needs an entry in the table for every gameweek they play in.
class FPLStats(DatabaseManager):
    def __init__(self, fplID: int):
        self.fplID = fplID
        
    def populateDatabase(self):
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
            'creativity', 'threat', 'value', 'yellow_cards']]
            
            # only update the database if there is a more recent round of fixtures to enter
            
            try:
                # get the record containing the most recent round of fixtures
                latestRound = FPLAPIStatsGameweek.objects.filter(fpl_id=self.fplID).order_by('-fpl_gameweekNumber').first()
                # use the value of round in that record
                latestRound = latestRound.fpl_gameweekNumber
            except (FPLAPIStatsGameweek.DoesNotExist, AttributeError):
                latestRound = 0
            
            # only update the database if there are newer rounds to add
            if int(max(stats['round'])) > latestRound:
                # TEAM AND POSITION NEED TO BE RETREIVED FROM GENERAL INFORMATION (NEW CLASS AND DATABASE TABLE NEEDED!)
                for i in range(len(stats['element'])):
                    # try:
                    if stats['round'][i] <= latestRound:
                        try: 
                            FPLAPIStatsGameweek.objects.get(fpl_id=self.fplID, fpl_gameweekNumber=stats['round'][i])
                            needsUpdate = False
                        except FPLAPIStatsGameweek.DoesNotExist:
                            needsUpdate = True
                        # if the team had a double gameweek this error would be thrown
                        except FPLAPIStatsGameweek.MultipleObjectsReturned:
                            needsUpdate = False
                    else:
                        needsUpdate = True

                    if needsUpdate:
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
                            fpl_yellow_cards = stats['yellow_cards'][i],
                            fpl_cost = stats['value'][i],
                            fpl_threat = stats['threat'][i],
                            fpl_influence = stats['influence'][i],
                            fpl_creativity = stats['creativity'][i]
                        )
                        row.save()
