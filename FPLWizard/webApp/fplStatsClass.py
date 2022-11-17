import requests
import time
from requests import ConnectionError
import pandas as pd

# used to find max value of a column in a table
from django.db.models import Max

from .models import FPLAPIStatsGameweek, APIIDDictionary

# A class that can access a player's stats by gameweek, as well as containing methods to update the FPLAPI database table
class fplStats():
    def __init__(self, fplID: int):
        self.fplID = fplID
        

    def getPlayerName(self):
        return FPLAPIStatsGameweek.objects.get(fpl_id=self.fplID).fpl_player_name

    def getPlayerAssists(self, gameweek: int):
        return FPLAPIStatsGameweek.objects.get(fpl_id=self.fplID, fplGameweekNumber=gameweek).fpl_assists

    def getPlayerGoalsConceded(self, gameweek:int):
        return FPLAPIStatsGameweek.objects.get(fpl_id=self.fplID, fplGameweekNumber=gameweek).fpl_goals_conceded

    def getPlayerCleanSheets(self, gameweek: int):
        return FPLAPIStatsGameweek.objects.get(fpl_id=self.fplID, fplGameweekNumber=gameweek).fpl_clean_sheets

    def getPlayerTotalPoints(self, gameweek: int):
        return FPLAPIStatsGameweek.objects.get(fpl_id=self.fplID, fplGameweekNumber=gameweek).fpl_total_points
    
    # This still needs to include gameweek to acocunt for interleague transfers occuring in the january transfer window
    def getPlayerTeamID(self, gameweek: int):
        return FPLAPIStatsGameweek.objects.get(fpl_id=self.fplID, fplGameweekNumber=gameweek).fpl_team

    def getMinutes(self, gameweek: int):
        return FPLAPIStatsGameweek.objects.get(fpl_id=self.fplID, fplGameweekNumber=gameweek).minutes
    
    def getGoals(self, gameweek: int):
        return FPLAPIStatsGameweek.objects.get(fpl_id=self.fplID, fplGameweekNumber=gameweek).goals

    def getPlayerPosition(self):
        return FPLAPIStatsGameweek.objects.get(fpl_id=self.fplID).fpl_position
    
    def getPlayerCost(self, gameweek: int):
        return FPLAPIStatsGameweek.objects.get(fpl_id=self.fplID, fplGameweekNumber=gameweek).fpl_cost
    
    def getPlayerThreat(self, gameweek: int):
        return FPLAPIStatsGameweek.objects.get(fpl_id=self.fplID, fplGameweekNumber=gameweek).fpl_threat
    
    def getPlayerInfluence(self, gameweek: int):
        return FPLAPIStatsGameweek.objects.get(fpl_id=self.fplID, fplGameweekNumber=gameweek).fpl_influence
    
    def getPlayerCreativity(self, gameweek: int):
        return FPLAPIStatsGameweek.objects.get(fpl_id=self.fplID, fplGameweekNumber=gameweek).fpl_creativity

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
            
            # only update the database if there is a more recent round of fixtures to enter
            
            # get the record containing the most recent round of fixtures
            latestRound = FPLAPIStatsGameweek.objects.order_by('-round').first()
            # use the value of round in that record
            latestRound = latestRound.round

            if int(max(stats['round'])) > latestRound:
                # TEAM AND POSITION NEED TO BE RETREIVED FROM GENERAL INFORMATION (NEW CLASS AND DATABASE TABLE NEEDED!)
                #for i in range(len(stats['element'])):
                    #try: 
                    #   FPLAPIStatsGameweek.objects.get(fpl_id=self.fplID, fpl_gameweek=stats['round'][i])
                    #  needsUpdate = False
                    # if no object with playerID and round exists
                    #except DoesNotExist:
                        #needsUpdate = True
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
                            fpl_team = 0,
                            fpl_position = 0,
                            fpl_cost = stats['value'][i],
                            fpl_threat = stats['threat'][i],
                            fpl_influence = stats['influence'][i],
                            fpl_creativity = stats['creativity'][i]
                        )
                        row.save()
            
