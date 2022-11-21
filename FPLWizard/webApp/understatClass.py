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
nest_asyncio.apply()

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
        async def main():
            async with aiohttp.ClientSession() as session:
                understat = Understat(session)

                player_matches = await understat.get_player_matches(
                    self.understatID, season=CURRENT_SEASON
                )
                return json.dumps(player_matches)
        
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())