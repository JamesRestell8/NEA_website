import pandas as pd
import time
import requests

from .models import PlayerTeamAndPosition


class PlayerGeneralInfoUpdater():
    def __init__(self) -> None:
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
                    xP=0
                )
                row.save()
