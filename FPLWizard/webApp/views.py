from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.template import loader

# Create your views here.

# Home/Welcome screen
def index(request):
    template = loader.get_template("webApp/index.html")
    context = {}
    return HttpResponse(template.render(context, request))


def allPlayers(request):
    template = loader.get_template("webApp/allPlayers.html")
    context = {
        'pageName': "All Players"
        }
    return HttpResponse(template.render(context, request))


def positions(request):
    template = loader.get_template("webApp/positions.html")
    context = {
        'pageName': 'Positions'
    }
    return HttpResponse(template.render(context, request))


def myFPL(request):
    template = loader.get_template("webApp/myFPL.html")
    context = {
        'pageName': "My FPL"
    }
    return HttpResponse(template.render(context, request))