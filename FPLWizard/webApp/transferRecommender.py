import pandas as pd


class TransferRecommender():
    def __init__(self, currentTeam: list, transferInfo: list, currentChips: pd.DataFrame) -> None:
        self.currentTeam = currentTeam
        self.transferInfo = transferInfo
        self.currentChips = currentChips