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
    
    def recommendChips(self):
        return ["Free Hit", "Triple Captain", "Bench Boost", "Wildcard"]
    
    # this function should return the players current budget, their team value, a list of transfer recommendations, and a list of chip recommnedations
    def getRecommendations(self) -> tuple:
        return (self.getBudget(), self.getTeamValue(), self.recommendTransfers(), self.recommendChips())