from .models import FPLAPIStatsGameweek

class fplStats():
    def __init__(self, fplID: int, gameweekNumber: int):
        self.fplID = fplID
        self.gameweekNumber = gameweekNumber
        self.isAggregate = False

        if self.gameweekNumber == 0:
            self.isAggregate = True
        
        # set defualt values to be populated later from the database
        self.fplPlayerName = ""
        self.minutes = 0
        self.goals = 0
        self.assists = 0
        self.goalsConceded = 0
        self.cleanSheets = 0
        self.totalPoints = 0
        self.teamID = 0
        self.position = 0
        self.cost = 0
        self.threat = 0
        self.influence = 0
        self.creativity = 0
        self.pointsPerGame = 0

    # INSERT GETTERS AND SETTERS FOR ALL ATTRIBUTES HERE
    
    def populateStats(self):
        row = FPLAPIStatsGameweek.objects.get(fpl_id=self.fplID)
