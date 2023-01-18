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
        position = PlayerTeamAndPosition.objects.get(playerID=fplID).position
        try:
            playerGameweeks = FPLAPIStatsGameweek.objects.filter(fpl_id=fplID)
            mostRecentGameweeks = playerGameweeks.order_by('-fpl_gameweekNumber')
            icts = []
            minutes = []
            cleanSheets = []
            count = 0
            while len(icts) != 5:
                if Fixture.objects.get(fixtureID=mostRecentGameweeks[count].fpl_fixtureID).homeTeamGoals == -1:
                    count += 1
                else:
                    ict = mostRecentGameweeks[count].fpl_influence + mostRecentGameweeks[count].fpl_creativity + mostRecentGameweeks[count].fpl_threat
                    mins = mostRecentGameweeks[count].fpl_minutes
                    cleanSheet = mostRecentGameweeks[count].fpl_clean_sheets
                    icts.append(ict)
                    minutes.append(mins)
                    cleanSheets.append(cleanSheet)
                    count += 1
            ictScore = self.averageList(icts)
            minutesScore = self.averageList(minutes)
            cleanSheetScore = self.averageList(cleanSheets)
        except IndexError:
            ictScore = 0
            minutesScore = 0
            cleanSheetScore = 0
        underlyings = self.getUnderlyings(fplID)
        xG = underlyings[0]
        xA = underlyings[1]
        xGChain = underlyings[2]
        return self.getForm(position, xG, xA, xGChain, cleanSheetScore, minutesScore, ictScore)

    def getForm(self, position: int, xG: float, xA: float, xGChain: float, cleanSheets: float, minutes: float, ICT: float) -> float:
        if position == 1:
            return (xGChain * 3) + (cleanSheets * 5) + (minutes / 60) + (ICT / 100)
        elif position == 2:
            return (xG * 4) + (xA * 4) + (cleanSheets * 5) + (minutes / 60) + (ICT / 50)
        elif position == 3:
            return (xG * 5) + (xA * 4) + (cleanSheets * 2) + (minutes / 60) + (ICT / 100)
        elif position == 4:
            return (xG * 5) + (xA * 3) + (minutes / 90) + (ICT / 100)
        else:
            return 0

    def getUnderlyings(self, fplID: int) -> tuple:
        try:
            understatID = APIIDDictionary.objects.get(fplID=fplID).understatID
        except APIIDDictionary.DoesNotExist:
            return 0, 0, 0
        
        try:
            playerGameweeks = UnderstatAPIStatsGameweek.objects.filter(understat_id=understatID)
            mostRecentGameweeks = playerGameweeks.order_by('-understat_fixtureID')
            xGs = []
            xAs = []
            xGChains = []
            count = 0
            while len(xGs) != 5:
                chain = mostRecentGameweeks[count].understat_xG_chain
                buildup = mostRecentGameweeks[count].understat_xG_buildup
                if chain >= buildup:
                    toUse = chain
                else:
                    toUse = buildup
                count += 1
                xGs.append(mostRecentGameweeks[count].understat_xG)
                xAs.append(mostRecentGameweeks[count].understat_xA)
                xGChains.append(toUse)
            xG = self.averageList(xGs)
            xA = self.averageList(xAs)
            xGc = self.averageList(xGChains)
        except IndexError:
            xG = 0
            xA = 0 
            xGc = 0
        return (xG, xA, xGc)

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
                print("Didn't exist")
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

