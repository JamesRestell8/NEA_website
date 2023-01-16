from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.template import loader
from datetime import datetime
from django.urls import reverse
from django.contrib import messages
import json

from .databaseUpdates import DatabaseUpdater
from .user import User
from .models import APIIDDictionary, FPLAPIStatsGameweek, PlayerTeamAndPosition, UnderstatAPIStatsGameweek, Team
import pandas as pd
from .forms import userTeamEntry
from FPLWizard.settings import MEDIA_ROOT
from .knapsackSolver import knapsackSolver

# Home/Welcome screen
def index(request):
    template = loader.get_template("webApp/index.html")
    # TODO: need to convert data from PlayerTeamAndPosition into a table that knapsackSolver understands
    playerTable = []
    players = PlayerTeamAndPosition.objects.all()
    for player in players:
        try:
            cost = FPLAPIStatsGameweek.objects.filter(fpl_id=player.playerID).order_by('-fpl_gameweekNumber').first().fpl_cost
            name = APIIDDictionary.objects.get(fplID=player.playerID).understatName
            playerTable.append([player.position, player.teamID, cost, player.xP, name])
        except AttributeError:
            pass
        except APIIDDictionary.DoesNotExist:
            pass

    knapsack = knapsackSolver(playerTable, 1000, 15, [])
    dreamTeam = knapsack.solveKnapsack()

    context = {
        'dreamTeam': dreamTeam[0],
        'total': dreamTeam[1],
        'nextGameweek': dreamTeam[2] + 1,
    }
    return HttpResponse(template.render(context, request))

def myFPL(request):
    template = loader.get_template("webApp/myFPL.html")

    team = []

    # it it's not GET, we know it's POST
    if request.method == "POST":
        form = userTeamEntry(request.POST)
        if form.is_valid():
            try:
                teamInfo = json.loads(form.cleanJSONField())
                print(teamInfo.keys())
                players = pd.DataFrame.from_dict(teamInfo['picks'])
                team.append(players.columns)
                chips = pd.DataFrame.from_dict(teamInfo['chips'])
                team.append(chips.columns)
                transfers = teamInfo['transfers']
                team.append(transfers)
            except ValueError:
                team.append("Error")
        else:
            print("Team is not valid :(")

    else:
        form = userTeamEntry()
    context = {
        'content': team,
        'form': form
    }
    return HttpResponse(template.render(context, request))


def goalkeepers(request):
    template = loader.get_template("webApp/positions.html")
    players = PlayerTeamAndPosition.objects.filter(position=1).order_by('-xP')
    info = []
    for player in players:
        xP = player.xP
        try:
            name = APIIDDictionary.objects.get(fplID=player.playerID).understatName
            info.append((name, xP))
        except APIIDDictionary.DoesNotExist:
            pass
    context = {
        'position': 'Goalkeeper',
        'players': info,
    }
    return HttpResponse(template.render(context, request))


def defenders(request):
    template = loader.get_template("webApp/positions.html")
    players = PlayerTeamAndPosition.objects.filter(position=2).order_by('-xP')
    info = []
    for player in players:
        xP = player.xP
        try:
            name = APIIDDictionary.objects.get(fplID=player.playerID).understatName
            info.append((name, xP))
        except APIIDDictionary.DoesNotExist:
            pass
    context = {
        'position': 'Defender',
        'players': info,
    }
    return HttpResponse(template.render(context, request))


def midfielders(request):
    template = loader.get_template("webApp/positions.html")
    players = PlayerTeamAndPosition.objects.filter(position=3).order_by('-xP')
    info = []
    for player in players:
        xP = player.xP
        try:
            name = APIIDDictionary.objects.get(fplID=player.playerID).understatName
            info.append((name, xP))
        except APIIDDictionary.DoesNotExist:
            pass
    context = {
        'position': 'Midfielder',
        'players': info,
    }
    return HttpResponse(template.render(context, request))


def attackers(request):
    template = loader.get_template("webApp/positions.html")
    players = PlayerTeamAndPosition.objects.filter(position=4).order_by('-xP')
    info = []
    for player in players:
        xP = player.xP
        try:
            name = APIIDDictionary.objects.get(fplID=player.playerID).understatName
            info.append((name, xP))
        except APIIDDictionary.DoesNotExist:
            pass

    context = {
        'position': 'Attacker',
        'players': info,
    }
    return HttpResponse(template.render(context, request))


def fplIDHelp(request):
    template = loader.get_template("webApp/fplIDHelp.html")
    context = {}
    return HttpResponse(template.render(context, request))

def teamStrength(request):
    template = loader.get_template("webApp/teamStrength.html")
    teams = Team.objects.all().order_by('-teamStrength')
    info = []
    for team in teams:
        info.append((team.teamName, int(team.teamStrength)))
    context = {
        "teams": info,
    }
    return HttpResponse(template.render(context, request))