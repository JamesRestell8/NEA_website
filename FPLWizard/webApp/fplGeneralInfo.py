import pandas as pd
import time
import requests
from django.db.models import Q

from .models import PlayerTeamAndPosition
from .models import FPLAPIStatsGameweek
from .models import APIIDDictionary
from .models import UnderstatAPIStatsGameweek
from .models import Fixture
from .models import Team
from .databaseManager import databaseManager
from .team import TeamUpdater

class PlayerGeneralInfoUpdater(databaseManager):
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
        toReturn += self.getUnderlyings(fplID)
        return float(toReturn)

    def getUnderlyings(self, fplID: int):
        try:
            understatID = APIIDDictionary.objects.get(fplID=fplID).understatID
        except APIIDDictionary.DoesNotExist:
            return 0
        
        try:
            playerGameweeks = UnderstatAPIStatsGameweek.objects.filter(understat_id=understatID)
            mostRecentGameweeks = playerGameweeks.order_by('-understat_fixtureID')
            scores = []
            count = 0
            while len(scores) != 5:
                chain = mostRecentGameweeks[count].understat_xG_chain
                buildup = mostRecentGameweeks[count].understat_xG_buildup
                if chain >= buildup:
                    toUse = chain
                else:
                    toUse = buildup
                scores.append(toUse * 2)
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
        print(len(info['id']))
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

            playerTeam = Team.objects.get(teamID=existing.teamID)
            playerTeamStrength = playerTeam.teamStrength

            # get all unplayed matches
            # exclude fixtures that are to be rescheduled
            unplayed = Fixture.objects.filter(homeTeamGoals=-1).exclude(gameweekNumber=-1)
            # get only the games that the players team is involved in
            unplayed = unplayed.filter(Q(homeTeamID = existing.teamID) | Q(awayTeamID = existing.teamID))

            unplayed = unplayed.order_by('gameweekNumber')
            nextMatch = unplayed[0]
            if nextMatch.homeTeamID == existing.teamID:
                isHome = True
                oppositionStrength = Team.objects.get(teamID=nextMatch.awayTeamID).teamStrength
            else:
                isHome = False
                oppositionStrength = Team.objects.get(teamID=nextMatch.homeTeamID).teamStrength
            # scale a players xP based on their win probability
            existing.xP = existing.form * ((TeamUpdater.getProbability(playerTeamStrength, oppositionStrength, isHome) / 2) + 0.5)
            existing.save()

