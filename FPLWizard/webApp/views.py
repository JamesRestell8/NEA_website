from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.template import loader

from .forms import fplIDForm
from .person import User

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
    fplID = ""
    email = ""
    password = ""
    team = ""
    if request.method == "POST":
        form = fplIDForm(request.POST)

        if form.is_valid():
            fplID = form.cleaned_data["fplID"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            # this is now a variable holding fplID, which can be used
            # to retrieve the user's FPL team from the API server
            # still need to figure out how the API works.
            user = User(email, password, fplID)
            team = user.getFplTeam()

    else:
        form = fplIDForm()
    
    
    context = {
        'pageName': "My FPL",
        'form': form,
        'fplID': fplID,
        'email': email,
        'password': password,
        'teamInfo': team
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