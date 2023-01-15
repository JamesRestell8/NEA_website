import pandas as pd
import time
import numpy


class knapsackSolver():
    def __init__(self, playerTable: list, budget: int, squadSize: int, answer: list):
        self.playerTable = playerTable
        self.budget = budget
        self.squadSize = squadSize
        self.answer = answer
    
    def checkTeams(self, items: list, limit: int) -> int:
        unique = []
        for item in items:
            if item not in unique:
                unique.append(item)

        count = [0 for i in range(len(unique))]

        for item in items:
            count[unique.index(item)] += 1

        for num in count:
            if num >= limit:
                return unique[count.index(num)]
        return 0


    def checkPositions(self, items) -> int:
        unique = [1, 2, 3, 4]

        count = [0 for i in range(len(unique))]
        for item in items:
            count[item - 1] += 1

        limits = [2, 5, 5, 3]
        answer = 0
        for i in range(len(count)):
            if count[i] == limits[i]:
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
            if row[2] != position:
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

    def homemadeKnapsackWithNames(self, budget: int, maxPlayers: int, table: list, answer: list):
        if len(answer) == 15:
            total = 0
            totalCost = 0
            for i in range(len(answer)):
                print(f"Player: {answer[i][4]} (Cost: {answer[i][2]} --- Points: {answer[i][3]})")
                total += answer[i][3]
                totalCost += answer[i][2]
            print(f"Max Points: {total}")
            print(f"Players used: {len(answer)}")
            print(f"Budget used: {totalCost}")
            return answer

        if len(answer) > 1:
            positions = []
            teams = []
            for entry in answer:
                positions.append(entry[0])
                teams.append(entry[1])
            # remove players who play in a position that is already full
            table = self.removePosition(table, self.checkPositions(positions))

            # remove players who play for a team who already have 3 players in the team
            table = self.removeTeam(table, self.checkTeams(teams, 3))

        # only populate the density values the first time the function is called
        if len(answer) == 0:
            for i in range(len(table)):
                table[i].append(int(table[i][5]) / int(table[i][3]))

        # sort by descending density values
        table = self.mergeSort2DBy(table, 6)
        # ensures that the algorithm never buys a player that is so expensive that it can't fill in the rest of the squad
        minBudget = 45 * (maxPlayers - 1) 
        if maxPlayers != 0:
            # makes sure that the algo makes the most of its budget near the end of squad selection
            minNextPlayerPrice = (budget / maxPlayers) - 20

            # ensures that the min price never crashes the algorithm by being more than the most expensive player
            if minNextPlayerPrice > 95:
                minNextPlayerPrice = 95

            # add the first player that is affordable, and above the minimum price value
            for i in range(len(table)):
                if (budget - table[i][3] >= minBudget) and table[i][3] >= minNextPlayerPrice:
                    answer.append((table[i][2], table[i][1], table[i][3], table[i][5], table[i][0]))
                    cost = table[i][3]
                    table.pop(i)
                    # call the function again, with updated parameters
                    return self.homemadeKnapsackWithNames(budget - cost, maxPlayers - 1, table, answer)
    def solveKnapsack(self):
        return self.homemadeKnapsackWithNames(self.budget, self.squadSize, self.playerTable, self.answer)