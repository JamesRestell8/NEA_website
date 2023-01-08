from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.template import loader
from datetime import datetime
from django.urls import reverse
from django.contrib import messages

from .databaseUpdates import DatabaseUpdater
from .user import User
from .models import APIIDDictionary, FPLAPIStatsGameweek, UnderstatAPIStatsGameweek
import pandas as pd
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

    content = [MEDIA_ROOT]


    # it it's not GET, we know it's POST
    if request.method == "POST":
        pass
        # Make a new instance of user class, and use method to access FPL team
        #user = User(email, password, fplID)
        #team = user.getFplTeam()

        #if user.isValid():
        ## this line excludes information about bonus chips and transfers which will be needed
        #    table = team['picks']
        #    for i in range(len(table)):
        #        num = table[i].get('element')
        #        player = APIIDDictionary.objects.get(fplID=num)
        #        playerPoints = FPLAPIStatsGameweek.objects.get(fpl_id=num).fpl_total_points
        #        toPrint.append(player.understatName + " " + playerPoints)
        #else:
        #    valid = False
        #    toPrint = "Invalid FPL login details"
    context = {
        'content': content
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