import requests
import time
from requests.exceptions import ConnectionError
import pandas as pd
import asyncio
import json
import aiohttp
import nest_asyncio
import sys

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
        # code to fix an issue with asyncio package found here: https://github.com/encode/httpx/issues/914
        if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        async def main(understatID: int):
            async with aiohttp.ClientSession() as session:
                print("in loop")
                understat = Understat(session)
                player_matches = await understat.get_player_matches(
                            understatID, season="2022")
            return (json.dumps(player_matches))
        
        loop = asyncio.run((main(self.understatID)))

        data = pd.read_json(loop)
        try:
            data = data[['shots', 'xG', 'id', 'xA', 'key_passes', 'npxG', 'xGChain', 'xGBuildup']]
        except KeyError: 
            print(data.columns)
            return

        try:
            latestRound = UnderstatAPIStatsGameweek.objects.filter(understat_id=self.understatID).order_by('-understat_fixtureID').first()
            latestRound = latestRound.id
        except (UnderstatAPIStatsGameweek.DoesNotExist, AttributeError):
            latestRound = 0
        
        if int(max(data['id'])) > latestRound:
            for i in range(len(data['id'])):
                if data['id'][i] <= latestRound:
                    try:
                        UnderstatAPIStatsGameweek.objects.get(understat_id=self.understatID, understat_fixtureID=data['id'][i])
                        needsUpdate = False
                    except UnderstatAPIStatsGameweek.DoesNotExist:
                        needsUpdate = True
                else:
                    needsUpdate = True
                if needsUpdate:
                    print("adding row...")
                    row = UnderstatAPIStatsGameweek(
                        understat_id = self.understatID,
                        understat_playerName = APIIDDictionary.objects.get(understatID=self.understatID).understatName,
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
