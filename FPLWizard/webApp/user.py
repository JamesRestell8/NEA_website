import json
import requests
from urllib3.exceptions import InsecureRequestWarning
from .models import APIIDDictionary

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
class User():
    def __init__(self, team: list):
        self.team = team
        self.valid = True
    
    def isValid(self):
        # for every player in the team that has been submitted, check that the player is actually in the database
        # if any player isn't in the database, the team is invalid
        for player in self.team:
            try:
                APIIDDictionary.objects.get(fplName=player)
            except APIIDDictionary.DoesNotExist:
                return False
        return True
