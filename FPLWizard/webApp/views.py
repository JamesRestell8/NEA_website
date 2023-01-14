from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.template import loader
from datetime import datetime
from django.urls import reverse
from django.contrib import messages

from .databaseUpdates import DatabaseUpdater
from .user import User
from .models import APIIDDictionary, FPLAPIStatsGameweek, UnderstatAPIStatsGameweek, Team
import pandas as pd
from .forms import userTeamEntry
from FPLWizard.settings import MEDIA_ROOT

# Home/Welcome screen
def index(request):
    template = loader.get_template("webApp/index.html")
    context = {}
    return HttpResponse(template.render(context, request))


def positions(request):
    template = loader.get_template("webApp/positions.html")
    context = {
        'pageName': 'Positions'
    }
    return HttpResponse(template.render(context, request))


def csvTeamToPandas(file):
    pass


def myFPL(request):
    template = loader.get_template("webApp/myFPL.html")

    team = []

    # it it's not GET, we know it's POST
    if request.method == "POST":
        form = userTeamEntry(request.POST)
        if form.is_valid():
            for i in range(11):
                team.append(form.cleaned_data[f"player{i+1}"])
            for i in range(4):
                team.append(form.cleaned_data[f"sub{i+1}"])
        
        user = User(team)
        if user.isValid():
            print("Team is valid!")
            for i in range(len(team)):
                team[i] = APIIDDictionary.objects.get(fplName=team[i]).understatName
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
    context = {
        'pageName': 'goalkeepers'
    }
    return HttpResponse(template.render(context, request))


def defenders(request):
    template = loader.get_template("webApp/positions.html")
    context = {
        'pageName': 'defenders'
    }
    return HttpResponse(template.render(context, request))


def midfielders(request):
    template = loader.get_template("webApp/positions.html")
    context = {
        'pageName': 'midfielders'
    }
    return HttpResponse(template.render(context, request))


def attackers(request):
    template = loader.get_template("webApp/positions.html")
    context = {
        'pageName': 'attackers'
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