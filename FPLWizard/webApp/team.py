import requests
import time
from requests import ConnectionError
import pandas as pd

from .models import Team


class TeamUpdater():
    def __init__(self):
        pass

    def populateDatabase(self):
        url = "https://fantasy.premierleague.com/api/bootstrap-static/"

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
        
        team = pd.DataFrame(r['teams'])
        team = team[['id', 'short_name']]


        for i in range(len(team['id'])):
            currentTeam = team['id'][i]
            currentName = team['short_name'][i]
            # add the team if the team isn't already in the database
            try:
                Team.objects.get(teamID=currentTeam)
            except Team.DoesNotExist:
                row = Team(
                    teamID=currentTeam,
                    teamName=currentName,
                    teamStrength=0
                    )
                row.save()