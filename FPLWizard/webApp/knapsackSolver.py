import pandas as pd
import time
import numpy
from django.db.models import Q

from .models import Team, FPLAPIStatsGameweek, Fixture

class knapsackSolver():
    def __init__(self, playerTable: list, budget: int, squadSize: int, answer: list, positionsDone: list, teamsDone: list):
        self.playerTable = playerTable
        self.budget = budget
        self.squadSize = squadSize
        self.answer = answer
        self.positionsDone = positionsDone
        self.teamsDone = teamsDone
    
    def checkTeams(self, items: list, limit: int, toExclude: list) -> int:
        # a list of all the team codes (numbers 1-20)
        unique = [i + 1 for i in range(20)]
        # a list to keep a track of how many players have been picked from team i - 1.
        count = [0 for i in range(len(unique))]

        for item in items:
            count[unique.index(item)] += 1
        for num in count:
            if num >= limit:
                if unique[count.index(num)] not in toExclude:
                    return unique[count.index(num)]
        return 0


    def checkPositions(self, items: list, toExclude: list) -> int:
        # positions codes - GK, DEF, MID, ATT
        unique = [1, 2, 3, 4]
        # keep track of how many players of each position have been found
        count = [0 for i in range(len(unique))]
        for item in items:
            count[item - 1] += 1
        # these are the position limits for the FPL squad - in order of GK, DEF, MID, ATT
        limits = [2, 5, 5, 3]
        answer = 0
        for i in range(len(count)):
            # flag a position as done if the position limit has been reached, and it hasn't already been flagged
            if count[i] == limits[i] and (i + 1) not in toExclude:
                answer = i + 1
        return answer


    def getDensities(self, costs: list, values: list) -> list:
        answer = []
        for i in range(len(costs)):
            answer.append(int(values[i]) / int(costs[i]))
        return answer


    def get2DArray(self, table: pd.DataFrame) -> list:
        return table.to_numpy().tolist()


    def removePosition(self, table: list, position: int) -> list:
        answer = []
        for row in table:
            if row[0] != position:
                answer.append(row)
        return answer

    def getNextGameweek(self):
        return FPLAPIStatsGameweek.objects.all().order_by('-fpl_gameweekNumber').first().fpl_gameweekNumber

    # merge sort a 2D array based on a given index
    def mergeSort2DBy(self, table: list, index: int) -> list:
        if len(table) > 1:
            mid = len(table) // 2

            L = table[:mid]
            R = table[mid:]

            self.mergeSort2DBy(L, index)
            self.mergeSort2DBy(R, index)

            i = j = k = 0

            while i < len(L) and j < len(R):
                if L[i][index] >= R[j][index]:
                    table[k] = L[i]
                    i += 1
                else:
                    table[k] = R[j]
                    j += 1
                k += 1

            while i < len(L):
                table[k] = L[i]
                i += 1
                k += 1

            while j < len(R):
                table[k] = R[j]
                j += 1
                k += 1
        return table
    
    def getOpposition(self, teamID: int) -> str:
        teamFixtures = Fixture.objects.filter(homeTeamGoals=-1).exclude(gameweekNumber=-1)
        teamFixtures = teamFixtures.filter(Q(homeTeamID=teamID) | Q(awayTeamID=teamID))
        teamFixtures = teamFixtures.order_by('gameweekNumber')
        nextMatch = teamFixtures.first()
        if nextMatch.homeTeamID == teamID:
            nextOpponentName = Team.objects.get(teamID=nextMatch.awayTeamID).teamName + " (H)"
        else:
            nextOpponentName = Team.objects.get(teamID=nextMatch.homeTeamID).teamName + " (A)"
        return nextOpponentName


    # all tables should be indexed as follows [position, team, cost, xP, name, nextOpposition]
    def homemadeKnapsackWithNames(self, budget: int, maxPlayers: int, table: list, answer: list, positionsDone: list, teamsDone: list):
        if len(answer) == 15:
            total = 0
            totalCost = 0
            temp = []
            for i in range(len(answer)):
                print(f"Player: {answer[i][4]} (Cost: {answer[i][2]} --- Points: {answer[i][3]}) - Position: {answer[i][0]}")
                total += answer[i][3]
                totalCost += answer[i][2]
                temp.append((answer[i][4], answer[i][1], answer[i][0], answer[i][3], answer[i][2], self.getOpposition(answer[i][1])))
            
            temp = self.mergeSort2DBy(temp, 2)
            positions = {
                1: "GK",
                2: "DEF",
                3: "MID",
                4: "ATT",
            }
            toReturn = []
            for entry in temp:
                toReturn.append((entry[0], Team.objects.get(teamID=entry[1]).teamName, positions.get(entry[2]), entry[3], entry[4], entry[5]))
            print(f"Max Points: {total}")
            print(f"Players used: {len(answer)}")
            print(f"Budget used: {totalCost}")
            return (toReturn, total, self.getNextGameweek())

        if len(answer) > 1:
            positions = []
            teams = []
            for entry in answer:
                positions.append(entry[0])
                teams.append(entry[1])
            # remove players who play in a position that is already full
            positionToRemove = self.checkPositions(positions, positionsDone) 
            table = self.removePosition(table, positionToRemove)
            if positionToRemove != 0:
                positionsDone.append(positionToRemove)
            # remove players who play for a team who already have 3 players in the team
            teamToRemove = self.checkTeams(teams, 3, teamsDone)
            if teamToRemove != 0:
                teamsDone.append(teamToRemove)

        # only populate the density values the first time the function is called
        if len(answer) == 0 or len(answer) == 14:
            for i in range(len(table)):
                table[i].append(int(table[i][3]) / int(table[i][2]))

        # ensures that the algorithm never buys a player that is so expensive that it can't fill in the rest of the squad
        minBudget = 45 * (maxPlayers - 1)

        if len(answer) == 14:
            # on the last pick, we don't need to maximise value, we just want the most points
            table = self.mergeSort2DBy(table, 3)
            minNextPlayerPrice = 40
        else:
            # sort by descending density values
            table = self.mergeSort2DBy(table, 5)
            minNextPlayerPrice = (budget / maxPlayers) - 30
            costs = []
            for entry in table:
                costs.append(entry[2])
            maxPriceRemaining = max(costs)

            # ensures that the min price never crashes the algorithm by being more than the most expensive player
            if minNextPlayerPrice > maxPriceRemaining:
                minNextPlayerPrice = maxPriceRemaining - 10
        
        if maxPlayers != 0:
            # makes sure that the algo makes the most of its budget near the end of squad selection

            # add the first player that is affordable, and above the minimum price value
            for i in range(len(table)):
                if (budget - table[i][2] >= minBudget) and table[i][2] >= minNextPlayerPrice and table[i][1] not in teamsDone and table[i][0] not in positionsDone:
                    answer.append((table[i][0], table[i][1], table[i][2], table[i][3], table[i][4]))
                    cost = table[i][2]
                    table.pop(i)
                    # call the function again, with updated parameters
                    return self.homemadeKnapsackWithNames(budget - cost, maxPlayers - 1, table, answer, positionsDone, teamsDone)
    
    def solveKnapsack(self):
        return self.homemadeKnapsackWithNames(self.budget, self.squadSize, self.playerTable, self.answer, self.positionsDone, self.teamsDone)
