import pandas as pd
import time
import numpy

from .models import Team

class knapsackSolver():
    def __init__(self, playerTable: list, budget: int, squadSize: int, answer: list):
        self.playerTable = playerTable
        self.budget = budget
        self.squadSize = squadSize
        self.answer = answer
        self.positionsDone = []
        self.teamsDone = []
    
    def checkTeams(self, items: list, limit: int, toExclude: list) -> int:
        unique = []
        for item in items:
            if item not in unique:
                unique.append(item)

        count = [0 for i in range(len(unique))]

        for item in items:
            count[unique.index(item)] += 1

        for num in count:
            if num >= limit:
                if unique[count.index(num)] not in toExclude:
                    return unique[count.index(num)]
        return 0


    def checkPositions(self, items: list, toExclude: list) -> int:
        unique = [1, 2, 3, 4]

        count = [0 for i in range(len(unique))]
        for item in items:
            count[item - 1] += 1

        limits = [2, 5, 5, 3]
        answer = 0
        for i in range(len(count)):
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


    def removeTeam(self, table: list, team: int) -> list:
        for row in table:
            if row[1] == team:
                table.pop(table.index(row)) 
        return table

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

    def homemadeKnapsackWithNames(self, budget: int, maxPlayers: int, table: list, answer: list, positionsDone: list, teamsDone: list):
        print(len(answer))
        if len(answer) == 15:
            total = 0
            totalCost = 0
            temp = []
            for i in range(len(answer)):
                print(f"Player: {answer[i][4]} (Cost: {answer[i][2]} --- Points: {answer[i][3]}) - Position: {answer[i][0]}")
                total += answer[i][3]
                totalCost += answer[i][2]
                temp.append((answer[i][4], answer[i][1], answer[i][0], answer[i][3]))
            
            temp = self.mergeSort2DBy(temp, 2)
            positions = {
                1: "GK",
                2: "DEF",
                3: "MID",
                4: "ATT",
            }
            toReturn = []
            for entry in temp:
                toReturn.append((entry[0], Team.objects.get(teamID=entry[1]).teamName, positions.get(entry[2]), entry[3]))
            print(f"Max Points: {total}")
            print(f"Players used: {len(answer)}")
            print(f"Budget used: {totalCost}")
            return (toReturn, total)

        if len(answer) > 1:
            positions = []
            teams = []
            for entry in answer:
                positions.append(entry[0])
                teams.append(entry[1])
            # remove players who play in a position that is already full
            positionToRemove = self.checkPositions(positions, positionsDone) 
            table = self.removePosition(table, positionToRemove)
            positionsDone.append(positionToRemove)
            # remove players who play for a team who already have 3 players in the team
            teamToRemove = self.checkTeams(teams, 3, teamsDone)
            table = self.removeTeam(table, teamToRemove)
            teamsDone.append(teamToRemove)

        # only populate the density values the first time the function is called
        if len(answer) == 0:
            for i in range(len(table)):
                table[i].append(int(table[i][3]) / int(table[i][2]))

        # sort by descending density values
        table = self.mergeSort2DBy(table, 5)
        # ensures that the algorithm never buys a player that is so expensive that it can't fill in the rest of the squad
        minBudget = 45 * (maxPlayers - 1)
        print(len(table))
        if maxPlayers != 0:
            # makes sure that the algo makes the most of its budget near the end of squad selection
            minNextPlayerPrice = (budget / maxPlayers) - 20
            costs = []
            for entry in table:
                costs.append(entry[2])
            maxPriceRemaining = max(costs)

            # ensures that the min price never crashes the algorithm by being more than the most expensive player
            if minNextPlayerPrice > maxPriceRemaining:
                minNextPlayerPrice = maxPriceRemaining - 10
            # add the first player that is affordable, and above the minimum price value
            for i in range(len(table)):
                print(table[i][4])
                if (budget - table[i][2] >= minBudget) and table[i][2] >= minNextPlayerPrice:
                    answer.append((table[i][0], table[i][1], table[i][2], table[i][3], table[i][4]))
                    cost = table[i][2]
                    table.pop(i)
                    # call the function again, with updated parameters
                    return self.homemadeKnapsackWithNames(budget - cost, maxPlayers - 1, table, answer, positionsDone, teamsDone)
    
    def solveKnapsack(self):
        return self.homemadeKnapsackWithNames(self.budget, self.squadSize, self.playerTable, self.answer, self.positionsDone, self.teamsDone)