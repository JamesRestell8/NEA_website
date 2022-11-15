from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.template import loader
from datetime import datetime

from .forms import fplIDForm
from .databaseUpdates import DatabaseUpdater
from .user import User
from .models import APIIDDictionary
import pandas as pd


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


def myFPL(request):
    template = loader.get_template("webApp/myFPL.html")

    # set default values for first visit to the page
    fplID = ""
    email = ""
    password = ""
    toPrint = []
    valid = True
    if request.method == "POST":
        form = fplIDForm(request.POST)

        if form.is_valid():
            fplID = form.cleaned_data["fplID"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
        
            # Make a new instance of user class, and use method to access FPL team
            user = User(email, password, fplID)
            team = user.getFplTeam()

            if user.isValid():
            # this line excludes information about bonus chips and transfers which will be needed
                table = team['picks']
                for i in range(len(table)):
                    num = table[i].get('element')
                    player = APIIDDictionary.objects.get(fplID=num)
                    toPrint.append(player.understatName)
            else:
                valid = False
                table = team
    
    else:
        form = fplIDForm()
    
    db = DatabaseUpdater()

    db.setApiIdDictionary()
    db.populateAllFPLPlayerStatsByGameweek()

    # variables to send to HTML template
    context = {
        'pageName': "My FPL",
        'form': form,
        'fplID': fplID,
        'email': email,
        'password': list(password),
        'teamInfo': toPrint,
        'valid': valid
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