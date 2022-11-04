from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

#  A Table to store the data retrieved from the FPL API
class FPLAPIStatsGameweek(models.Model):
    # Primary key will be the code that the FPL API uses for the Player
    fpl_id = models.IntegerField(primary_key=True, verbose_name="FPL ID")

    #  all fields are NOT NULL by default
    fpl_player_name = models.CharField(max_length=100, verbose_name='Player Name')
    fpl_minutes = models.IntegerField(default=0, verbose_name='Minutes')
    fpl_assists = models.IntegerField(default=0, verbose_name='Assists')
    fpl_goals = models.IntegerField(default=0, verbose_name='Goals')
    fpl_clean_sheets = models.IntegerField(default=0, verbose_name='Clean Sheets')
    fpl_goals_conceded = models.IntegerField(default=0, verbose_name='Goals Conceded')
    fpl_total_points = models.IntegerField(default=0, verbose_name='Total Points')
    fpl_team = models.IntegerField(verbose_name='Team') # should be a number 1-20
    fpl_position = models.IntegerField(verbose_name='Position') # should be a number 1-4

    fpl_cost = models.FloatField(verbose_name='Cost')
    fpl_threat = models.FloatField(verbose_name='Threat')
    fpl_influence = models.FloatField(verbose_name='Influence')
    fpl_creativity = models.FloatField(verbose_name='Creativity')
    fpl_ppg = models.FloatField(verbose_name='Points Per Game')


# A table to store player data retrieved from the understat API. Similar function to the table above
class UnderstatAPIStatsGameweek(models.Model):
    # primary key will be the ID that the understat API uses to refer to the player
    understat_id = models.IntegerField(primary_key=True, verbose_name='Understat ID')

    # player stats below ('XG' = 'Expected Goals')
    understat_npxg = models.FloatField(verbose_name='Non-penalty xG')
    understat_xG = models.FloatField(verbose_name='xG')
    understat_xA = models.FloatField(verbose_name='xA')
    understat_key_passes = models.IntegerField(verbose_name='Key Passes')
    understat_xG_chain = models.FloatField(verbose_name='xG Chain')
    understat_xG_buildup = models.FloatField(verbose_name='xG Buildup')
    understat_shots = models.IntegerField(verbose_name='Shots')
    understat_yellow_cards = models.IntegerField(verbose_name='Yellow Cards')


class Gameweek():
    gameweekNumber = models.IntegerField(primary_key=True, verbose_name='Gameweek No.')
    endDeadline = models.DateTimeField()


class Fixture():
    # primary key will be autogenerated, exact value isn't important
    pass




class APIIDDictionary():
    playerID = models.IntegerField(primary_key=True)
    fplID = models.IntegerField(verbose_name="FPL ID")
    understatID = models.IntegerField(verbose_name='Understat ID')


class PlayerTeam():
    # django doesn't have support for composite foreign primary keys, so we will make an 
    # id column which will auto_increment, and let the other two just be foreign keys,
    # making this a de-facto composite foreign primary key.
    num = models.IntegerField(primary_key=True)
    playerID = models.ForeignKey(APIIDDictionary, db_column='playerID', verbose_name="Player ID", on_delete=models.CASCADE) 
    # on_delete = models.CASCADE means if the foreign object is deleted, the child object is also deleted
    teamID = models.ForeignKey(Team, db_column="teamID", verbose_name='Team ID', on_delete=models.CASCADE)


class Team():
    teamID = models.IntegerField(primary_key=True)
    teamName = models.CharField(max_length=100)
    leaguePos = models.IntegerField(verbose_name='League Position', validators=[MinValueValidator(0),MaxValueValidator(21)])

