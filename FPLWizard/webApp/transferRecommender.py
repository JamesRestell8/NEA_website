import pandas as pd


class TransferRecommender():
    def __init__(self, currentTeam: list, transferInfo: dict, currentChips: pd.DataFrame) -> None:
        self.currentTeam = currentTeam
        self.transferInfo = transferInfo
        self.currentChips = currentChips
    
    def getBudget(self):
        return self.transferInfo.get("bank")

    def getTeamValue(self):
        return self.transferInfo.get("value")
    
    def recommendTransfers(self):
        return ["Mbappe to Liverpool"]
    
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