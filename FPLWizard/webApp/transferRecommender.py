import pandas as pd

from .models import PlayerTeamAndPosition, FPLAPIStatsGameweek, APIIDDictionary
from .knapsackSolver import knapsackSolver

class TransferRecommender():
    def __init__(self, currentTeam: list, transferInfo: dict, currentChips: pd.DataFrame) -> None:
        self.currentTeam = currentTeam
        self.transferInfo = transferInfo
        self.currentChips = currentChips
    
    def getBudget(self):
        return self.transferInfo.get("bank")

    def getTeamValue(self):
        return self.transferInfo.get("value")
    
    def getTeamWithoutPlayer(self, playerToRemove: list, team: list) -> list:
        toReturn = []
        for item in team:
            if item[4] != playerToRemove[4]:
                toReturn.append(item)
        
        return toReturn

    def getAddedPlayer(self, oldTeam: list, newTeam: list):
        oldTeamNames = []
        for player in oldTeam:
            oldTeamNames.append(player[4])

        for player in newTeam:
            if player[0] not in oldTeamNames:
                return player
        return ["Error" for i in range(4)]

    def getTeamsDone(self, teamPlayers: list) -> list:
        unique = [i + 1 for i in range(20)]
        count = [0 for i in range(len(unique))]
        for item in teamPlayers:
            count[unique.index(item[1])] += 1
        
        toReturn = []
        index = 0
        for num in count:
            if num >= 3:
                toReturn.append(unique[index])
            index += 1
        return toReturn

    def recommendTransfers(self):
        # knapsack algo requires [position, team, cost, xP, name]
        knapsackFriendlyTeam = []
        for player in self.currentTeam:
            currentPlayer = PlayerTeamAndPosition.objects.get(playerID=player[0])
            currentPlayerInfo = [
                currentPlayer.position, 
                currentPlayer.teamID,
                FPLAPIStatsGameweek.objects.filter(fpl_id=player[0]).order_by('-fpl_gameweekNumber').first().fpl_cost,
                currentPlayer.xP,
                APIIDDictionary.objects.get(fplID=player[0]).understatName,
            ]
            knapsackFriendlyTeam.append(currentPlayerInfo)
        
        # get all available players in here
        playerTable = []
        recommedations = []
        players = PlayerTeamAndPosition.objects.all()
        # get the user's squad as a 2D array in playerTable
        for player in players:
            try:
                cost = FPLAPIStatsGameweek.objects.filter(fpl_id=player.playerID).order_by('-fpl_gameweekNumber').first().fpl_cost
                name = APIIDDictionary.objects.get(fplID=player.playerID).understatName
                toAdd = True
                for existingPlayer in knapsackFriendlyTeam:
                    if name == existingPlayer[4]:
                        toAdd = False
                if toAdd:
                    playerTable.append([player.position, player.teamID, cost, player.xP, name])
            except AttributeError:
                pass
            except APIIDDictionary.DoesNotExist:
                pass
        
        # an array of 2D arrays, each representing a 14 man team with one addition to be made
        # for every player, if their xP is less than 4, remove that player from the team, and
        # get the knapsack algorithm to recommend a 15th player to replace them with.
        for player in knapsackFriendlyTeam:
            if player[3] <= 4:
                newTeam = self.getTeamWithoutPlayer(player, knapsackFriendlyTeam)

                newTeamNames = []
                newTeamTeams = []
                for playerName in newTeam:
                    newTeamNames.append(playerName[4])
                    newTeamTeams.append(playerName[1])

                positionsDone = []
                teamsDone = []
                for i in range(4):
                    if (i + 1) != player[0]:
                        positionsDone.append(i + 1)
                teamsDone = self.getTeamsDone(newTeam)

                optimisedTeam = knapsackSolver(playerTable, self.getBudget() + player[2], 1, newTeam, positionsDone, teamsDone)
                dreamTeam = optimisedTeam.solveKnapsack()
                
                # find the player that was added
                newPlayer = "Error"
                for dreamTeamPlayer in dreamTeam[0]:
                    print(dreamTeamPlayer[0])
                    if dreamTeamPlayer[0] not in newTeamNames:
                        newPlayer = dreamTeamPlayer[0]
                        recommedations.append(f"Transfer OUT {player[4]} for {newPlayer}")

        return recommedations

    
    def chip(self, chipName: str) -> str:
        userTotal = 0
        for entry in self.currentTeam:
            userTotal += entry[4]
        
        if chipName == "bboost":
            benchPlayers = self.currentTeam[-4:]
            benchTotal = 0
            for player in benchPlayers:
                benchTotal += player[4]
            if benchTotal >= 15:
                return f"Activate this week for an expected {benchTotal} extra points."
            else:
                return f"Don't play this week, will only gain an expected {benchTotal} extra points."
        elif chipName == "freehit":
            if userTotal <= 70:
                return f"Activate Free Hit this week, and copy the team of the week found on the home page."
            else:
                return f"Don't play this week, save it for a week where it will be more influential.'"
        elif chipName == "wildcard":
            if userTotal <= 75:
                return f"Activate Wildcard this week, and copy the team of the week found on the home page."
            else:
                return "Don't activate Wildcard - save it for a week where it will be more influential"
        elif chipName == "3xc":
            allPlayers = self.currentTeam
            maxPoints = 0
            bestPlayer = []
            for player in allPlayers:
                if player[4] >= maxPoints:
                    maxPoints = player[4]
                    bestPlayer = player
            if bestPlayer[4] >= 12:
                return f"Activate {bestPlayer[5]} as triple captain this week for an expected extra {2 * maxPoints} points."
            else:
                return f"Don't use this week, as it will only gain you an expected {maxPoints * 2} points."
        else:
            return "Invalid chip name"

    def recommendChips(self):
        # self.currentChips is a DataFrame with columns ['status_for_entry', 'played_by_entry', 'name', 'number', 'start_event', 'stop_event', 'chip_type']
        self.currentChips = self.currentChips[['status_for_entry', 'name']]
        self.currentChips = self.currentChips.to_numpy().tolist()
        wildcards = [item for item in self.currentChips]
        recs = []
        chipNames = {
            "wildcard": "Wildcard",
            "freehit": "Free Hit",
            "bboost": "Bench Boost",
            "3xc": "Triple Captain",
        }
        for wildcard in wildcards:
            if wildcard[0] == "available":
                recs.append(chipNames.get(wildcard[1]) + ": " + self.chip(wildcard[1]))
            else:
                recs.append(chipNames.get(wildcard[1]) + " has been used.")
            
        return recs
    # this function should return the players current budget, their team value, a list of transfer recommendations, and a list of chip recommnedations
    def getRecommendations(self) -> tuple:
        return (self.getBudget(), self.getTeamValue(), self.recommendTransfers(), self.recommendChips())