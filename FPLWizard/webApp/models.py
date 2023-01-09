from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

#  A Table to store the data retrieved from the FPL API
class FPLAPIStatsGameweek(models.Model):
    # compund primary key will be implemented in the way described below
    fpl_id = models.IntegerField(default=0, verbose_name="FPL ID")

    fpl_fixtureID = models.IntegerField(default=0, verbose_name='Fixture Number')
    fpl_gameweekNumber = models.IntegerField(default=0, verbose_name='Gameweek Number')

    #  all fields are NOT NULL by default
    fpl_player_name = models.CharField(max_length=100, verbose_name='Player Name')
    fpl_minutes = models.IntegerField(default=0, verbose_name='Minutes')
    fpl_assists = models.IntegerField(default=0, verbose_name='Assists')
    fpl_goals = models.IntegerField(default=0, verbose_name='Goals')
    fpl_clean_sheets = models.IntegerField(default=0, verbose_name='Clean Sheets')
    fpl_goals_conceded = models.IntegerField(default=0, verbose_name='Goals Conceded')
    fpl_total_points = models.IntegerField(default=0, verbose_name='Total Points')
    # should be a number 1-20
    fpl_team = models.IntegerField(verbose_name='Team', validators=[MinValueValidator(0), MaxValueValidator(21)]) 
    # should be a number 1-4
    fpl_position = models.IntegerField(verbose_name='Position', validators=[MinValueValidator(0), MaxValueValidator(5)]) 
    fpl_yellow_cards = models.IntegerField(verbose_name="Yellow Cards", default=0)
    fpl_cost = models.FloatField(verbose_name='Cost')
    fpl_threat = models.FloatField(verbose_name='Threat')
    fpl_influence = models.FloatField(verbose_name='Influence')
    fpl_creativity = models.FloatField(verbose_name='Creativity')

    def __str__(self):
        return self.fpl_player_name


# A table to store player data retrieved from the understat API. Similar function to the table above
class UnderstatAPIStatsGameweek(models.Model):

    understat_id = models.IntegerField(default=0, verbose_name='Understat ID')
    understat_fixtureID = models.IntegerField(default=0, verbose_name='Gameweek')

    understat_playerName = models.CharField(max_length=100, verbose_name = "Understat Name")
    # player stats below ('XG' = 'Expected Goals')
    understat_npxg = models.FloatField(verbose_name='Non-penalty xG')
    understat_xG = models.FloatField(verbose_name='xG')
    understat_xA = models.FloatField(verbose_name='xA')
    understat_key_passes = models.IntegerField(verbose_name='Key Passes')
    understat_xG_chain = models.FloatField(verbose_name='xG Chain')
    understat_xG_buildup = models.FloatField(verbose_name='xG Buildup')
    understat_shots = models.IntegerField(verbose_name='Shots')


class Team(models.Model):
    teamID = models.IntegerField(primary_key=True)
    teamName = models.CharField(max_length=100)

    def __str__(self):
        return self.teamName


class Fixture(models.Model):
    fixtureID = models.IntegerField(primary_key=True)
    homeTeamID = models.IntegerField(verbose_name='Home Team ID')
    awayTeamID = models.IntegerField(verbose_name='Away Team ID')
    homeTeamStrength = models.IntegerField(verbose_name="Home Team Strength")
    awayTeamStrength = models.IntegerField(verbose_name="Away Team Strength")
    homeTeamGoals = models.IntegerField(verbose_name="Home Team Goals")
    awayTeamGoals = models.IntegerField(verbose_name="Away Team Goals")
    gameweekNumber = models.IntegerField(verbose_name='Gameweek')


class APIIDDictionary(models.Model):
    playerID = models.IntegerField(primary_key=True)
    fplID = models.IntegerField(verbose_name="FPL ID")
    understatID = models.IntegerField(verbose_name='Understat ID')
    fplName = models.CharField(max_length=100, verbose_name="FPL Name")
    understatName = models.CharField(max_length=100, verbose_name="Understat Name")


class PlayerTeam(models.Model):
    # django doesn't have support for composite foreign primary keys, so we will make an 
    # id column which will auto_increment, and let the other two just be foreign keys,
    # making this a de-facto composite foreign primary key.
    num = models.IntegerField(primary_key=True)
    playerID = models.ForeignKey(APIIDDictionary, verbose_name="Player ID", on_delete=models.CASCADE) 
    # on_delete = models.CASCADE means if the foreign object is deleted, the child object is also deleted
    teamID = models.ForeignKey(Team, verbose_name='Team ID', on_delete=models.CASCADE)

    def __str__(self):
        return self.playerID + " - " + self.teamID

class TeamFixture(models.Model):
    # using same composite foreign primary key method as in PlayerTeam table
    # by defualt, Django names the ID field in a table "TableName_id"
    num = models.IntegerField(primary_key=True)
    fixtureID = models.ForeignKey(Fixture, verbose_name='Fixture ID', on_delete=models.CASCADE)
    teamID = models.ForeignKey(Team, verbose_name='Team ID', on_delete=models.CASCADE)


class XPGameweek(models.Model):
    # using same composite foreign primary key method as in PlayerTeam table
    num = models.IntegerField(primary_key=True)

    gameweekNumber = models.IntegerField(verbose_name='Gameweek')
    playerID = models.ForeignKey(APIIDDictionary, verbose_name='Player ID', on_delete=models.CASCADE)

    xP = models.FloatField(verbose_name='Expected Points')
    formCoefficient = models.FloatField(verbose_name='Form coefficient')
