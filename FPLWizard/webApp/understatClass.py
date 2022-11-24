import requests
import time
from requests.exceptions import ConnectionError
import pandas as pd
import asyncio
import json
import aiohttp
import nest_asyncio

from pandas.io.json import json_normalize

# this is how we will access the Understat API
from understat import Understat

from .models import APIIDDictionary, UnderstatAPIStatsGameweek
from FPLWizard.settings import CURRENT_SEASON

# initialise nest_asyncio, which allows asynchronous functions to be nested

class UnderstatStats():
    def __init__(self, understatID: int):
        self.understatID = understatID
    
    def getUnderstatID(self):
        return self.understatID
    
    def getNonPenaltyXG(self, gameweek: int):
        return UnderstatAPIStatsGameweek.objects.get(understat_id=self.understatID, understat_gameweekNumber=gameweek).understat_npxg
    
    # xg = expected goals: a statistic used in modern football analytics to provide a better indication of goal output
    def getXG(self, gameweek: int):
        return UnderstatAPIStatsGameweek.objects.get(understat_id=self.understatID, understat_gameweekNumber=gameweek).understat_xG
    
    # xa = expected assists: a statistic used in modern football analytics to provide a better indication of assist output
    def getXA(self, gameweek: int):
        return UnderstatAPIStatsGameweek.objects.get(understat_id=self.understatID, understat_gameweekNumber=gameweek).understat_xA
    
    def getKeyPasses(self, gameweek: int):
        return UnderstatAPIStatsGameweek.objects.get(understat_id=self.understatID, understat_gameweekNumber=gameweek).understat_key_passes
    
    def getXGChain(self, gameweek: int):
        return UnderstatAPIStatsGameweek.objects.get(understat_id=self.understatID, understat_gameweekNumber=gameweek).understat_xG_chain
    
    def getXGBuildup(self, gameweek: int):
        return UnderstatAPIStatsGameweek.objects.get(understat_id=self.understatID, understat_gameweekNumber=gameweek).understat_xG_buildup
    
    def getShots(self, gameweek: int):
        return UnderstatAPIStatsGameweek.objects.get(understat_id=self.understatID, understat_gameweekNumber=gameweek).understat_shots
    
    def getYellowCards(self, gameweek: int):
        return UnderstatAPIStatsGameweek.objects.get(understat_id=self.understatID, understat_gameweekNumber=gameweek).understat_yellow_cards
    
    def populateAllGameweeks(self):
        # NOT COMPLETE YET, TEST THIS IN A JUPYTER NOTEBOOK I WOULD SO YOU KNOW EXACTLY WHAT YOU'RE DEALING WITH.
        async def main(understatID: int):
            async with aiohttp.ClientSession() as session:
                print("in loop")
                understat = Understat(session)
                player_matches = await understat.get_player_matches(
                            understatID, season="2022")
            return (json.dumps(player_matches))
        

        loop = asyncio.run((main(self.understatID)))

        data = pd.read_json(loop)
        data = data[['goals', 'shots', 'time', 'xG', 'h_team', 'h_goals', 
                    'a_team', 'a_goals', 'date', 'id', 'xA', 'assists',
                    'key_passes', 'npxG', 'xGChain', 'xGBuildup']]

        try:
            latestRound = UnderstatAPIStatsGameweek.objects.filter(fpl_id=self.fplID).order_by('-id').first()
            latestRound = latestRound.id
        except (UnderstatAPIStatsGameweek.DoesNotExist, AttributeError):
            latestRound = 0
        
        if int(max(data['id'])) > latestRound:
            for i in range(len(data['goals'])):
                if data['id'][i] <= latestRound:
                    try:
                        UnderstatAPIStatsGameweek.objects.get(understat_id=self.understatID, understat_gameweekNumber=data['id'][i])
                        needsUpdate = False
                    except UnderstatAPIStatsGameweek.DoesNotExist:
                        needsUpdate = True
                else:
                    needsUpdate = True
                
                if needsUpdate:
                    row = UnderstatAPIStatsGameweek(
                        understat_id = self.understatID,
                        understat_playerName = APIIDDictionary.objects.get(fplID=self.understatID).understatName,
                        understat_fixtureID = data['id'][i],
                        understat_npxg = data['npxG'][i],
                        understat_xG = data['xG'][i],
                        understat_xA = data['xA'][i],
                        understat_key_passes = data['key_passes'][i],
                        understat_xG_chain = data['xGChain'][i],
                        understat_xG_buildup = data['xGBuildup'][i],
                        understat_shots = data['shots'][i],
                    )
                    row.save()
