import requests
import time
from requests import ConnectionError
import pandas as pd

from .models import Fixture


class FixtureUpdater():
    def __init__(self):
        pass

    def populateDatabase(self):
        url = "https://fantasy.premierleague.com/api/fixtures"

        found = False
        i = 0
        while not found and i < 30:
            try:
                r = requests.get(url)
                found = True
            except requests.exceptions.ConnectionError:
                time.sleep(1)
                i += 1
        
        if found:
            r = r.json()
        else:
            return
        
        fixtures = pd.DataFrame(r)
        fixtures = fixtures[['started', 'id', 'team_h', 'team_a', 'team_h_score', 'team_a_score', 'event']]

        for i in range(len(fixtures['id'])):
            needsUpdate = True
            # if the game hasn't been played, set scores to -1.
            if not fixtures['started'][i]:
                homeScore = -1
                awayScore = -1
            else:
                homeScore = int(fixtures['team_h_score'][i])
                awayScore = int(fixtures['team_a_score'][i])
            # if the game is being rescheduled (i.e. doesn't have a gameweek yet), set event to -1
            try:
                gameweekNumber = int(fixtures['event'][i])
            except ValueError:
                gameweekNumber = -1
            # if the fixture already exists, but has changed gameweeks, update that entry
            try:
                existingRecord = Fixture.objects.get(fixtureID=int(fixtures['id'][i]))
                existingGameweek = existingRecord.gameweekNumber
                if existingGameweek != gameweekNumber:
                    existingRecord.gameweekNumber = int(fixtures['event'][i])
                    needsUpdate = False
                else:
                    needsUpdate = False
                existingRecord.save()
            except Fixture.DoesNotExist:
                # if the fixture doesn't exist yet, add it.
                pass
        
            if needsUpdate:
                row = Fixture(
                    fixtureID=int(fixtures['id'][i]),
                    homeTeamID=int(fixtures['team_h'][i]),
                    awayTeamID=int(fixtures['team_a'][i]),
                    homeTeamStrength=0,
                    awayTeamStrength=0,
                    homeTeamGoals=homeScore,
                    awayTeamGoals=awayScore,
                    gameweekNumber=gameweekNumber
                )
                row.save()