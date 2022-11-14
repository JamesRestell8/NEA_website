import json
import requests


class User():
    def __init__(self, email: str, password: str, fplID: int):
        self.email = email
        self.password = password
        self.fplID = fplID
        self.valid = True
    
    def getEmail(self) -> str:
        return self.email
    
    def getPassword(self) -> str:
        return self.password
    
    def getFplID(self) -> int:
        return self.fplID
    
    def getFplTeam(self) -> str:
        session = requests.Session()

        # a dictionary of headers needed to make the request functional from https://stackoverflow.com/questions/62828619/how-to-login-in-fantasy-premier-league-using-python
        headers = {
            'authority': 'users.premierleague.com' ,
            'cache-control': 'max-age=0' ,
            'upgrade-insecure-requests': '1' ,
            'origin': 'https://fantasy.premierleague.com' ,
            'content-type': 'application/x-www-form-urlencoded' ,
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36' ,
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' ,
            'sec-fetch-site': 'same-site' ,
            'sec-fetch-mode': 'navigate' ,
            'sec-fetch-user': '?1' ,
            'sec-fetch-dest': 'document' ,
            'referer': 'https://fantasy.premierleague.com/my-team' ,
            'accept-language': 'en-US,en;q=0.9,he;q=0.8' ,
        }

        # authentication
        urlLogin = "https://users.premierleague.com/accounts/login/"

        data = {
            'password': self.password,
            'login': self.email,
            'redirect_uri': 'https://fantasy.premierleague.com/',
            'app': 'plfpl-web'
        }

        session.post(url=urlLogin, data=data, headers=headers)

        # now the session has been authenticated, we can request the user's team
        urlTeam = "https://fantasy.premierleague.com/api/my-team/" + str(self.fplID)
        team = session.get(url=urlTeam)
        toPrint = json.loads(team.content)

        if team.ok:
            return toPrint
        else:
            self.valid = False
            return "Invalid FPL login details"
    
    def isValid(self):
        return self.valid