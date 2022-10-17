from django.db import models


#  A Table to store the data retrieved from the FPL API
class FPLData(models.Model):
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
class UnderstatData(models.Model):
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
    understat_yello_cards = models.IntegerField(verbose_name='Yellow Cards')
