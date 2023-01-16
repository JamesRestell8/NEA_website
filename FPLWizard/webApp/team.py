import requests
import time
import pandas as pd
import math

from .models import Team
from .models import Fixture
from .databaseManager import databaseManager

class TeamUpdater(databaseManager):
    # return the probability that a team beats their opponent based on their elos
    # implementation of mainstream elo algorithm found in online games (chess etc.)
    # adjusted to favour the home team slightly (probabilities still add to 1)
    @staticmethod
    def getProbability(ratingTeam, ratingOpposition, isHome):
        if isHome:
            return (1.0 / (1 + math.pow(10, (ratingOpposition - ratingTeam) / 400))) * 1.1
        else:
            return 1 - TeamUpdater.getProbability(ratingOpposition, ratingTeam, True)

    def calculateElos(self) -> list:
        # Elo constant
        K = 100
        # set all teams elo to 1000 at the start of the season
        elos = [1000 for i in range(20)]
        # get all of the fixtures that have been played
        fixturesPlayed = Fixture.objects.exclude(homeTeamGoals=-1)
        # sort them by gameweek, with gameweek 1 first
        fixturesPlayed = fixturesPlayed.order_by('gameweekNumber')
        # for every fixture played, update the elo of both teams involved
        for i in range(len(fixturesPlayed)):
            # Get the IDs of the teams involved (also the index of the elo array)
            homeTeam = fixturesPlayed[i].homeTeamID
            awayTeam = fixturesPlayed[i].awayTeamID
            
            # get the amount of goals each team scored in the game
            homeScore = fixturesPlayed[i].homeTeamGoals
            awayScore = fixturesPlayed[i].awayTeamGoals

            # work out the probability of each team winning the game based on their elos
            homeProb = self.getProbability(elos[homeTeam - 1], elos[awayTeam - 1], True)
            awayProb = self.getProbability(elos[awayTeam - 1], elos[homeTeam - 1], False)

            # work out the actual result of the match (1 = win, 0.5 = draw, 0 = loss)
            if homeScore > awayScore:
                homeActual = 1
                awayActual = 0
            elif homeScore < awayScore:
                homeActual = 0
                awayActual = 1
            else:
                homeActual = 0.5
                awayActual = 0.5
            
            # adjust the elos of both teams based on the result and their initial elos
            elos[homeTeam - 1] = elos[homeTeam - 1] + K * (homeActual - homeProb)
            elos[awayTeam - 1] = elos[awayTeam - 1] + K * (awayActual - awayProb)
        return elos

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
        elos = self.calculateElos()
        
        for index, elo in enumerate(elos):
            team = Team.objects.get(teamID=index+1)
            team.teamStrength = elo
            team.save()
