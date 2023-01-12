import pandas as pd
import time
import requests

from .models import PlayerTeamAndPosition
from .models import FPLAPIStatsGameweek
from .models import Fixture


class PlayerGeneralInfoUpdater():
    def __init__(self) -> None:
        pass
    
    def updateForm(self, fplID: int) -> float:
        try:
            playerGameweeks = FPLAPIStatsGameweek.objects.filter(fpl_id=fplID)
            mostRecentGameweeks = playerGameweeks.order_by('-fpl_gameweekNumber')
            scores = []
            count = 0
            while len(scores) != 5:
                if Fixture.objects.get(fixtureID=mostRecentGameweeks[0].fpl_fixtureID).homeTeamGoals == -1:
                    count += 1
                else:
                    scores.append(mostRecentGameweeks[count].fpl_total_points)
                    count += 1
            toReturn = self.averageList(scores)
        except IndexError:
            toReturn = 0
        return float(toReturn)

    def averageList(self, array: list) -> float:
        total = 0
        count = 0
        for item in array:
            count += 1
            total += item
        return total / count

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
        
        info = pd.DataFrame(r['elements'])
        info = info[['id', 'team', 'element_type']]

        for i in range(len(info['id'])):
            try:
                existing = PlayerTeamAndPosition.objects.get(playerID=info['id'][i])
                # update the player if their information has changed
                currentTeam = info['team'][i]
                currentPos = info['element_type'][i]
                if existing.teamID != currentTeam:
                    existing.teamID = currentTeam
                if existing.position != currentPos:
                    existing.position = currentPos
                existing.save()
            # add the player if the player does not exist
            except PlayerTeamAndPosition.DoesNotExist:
                row = PlayerTeamAndPosition(
                    playerID=info['id'][i],
                    teamID=info['team'][i],
                    position=info['element_type'][i],
                    form=0,
                    xP=0
                )
                row.save()
                existing = PlayerTeamAndPosition.objects.get(playerID=info['id'][i])
            
            existing.form = self.updateForm(existing.playerID)
            existing.save()

