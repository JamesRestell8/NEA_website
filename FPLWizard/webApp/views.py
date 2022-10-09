from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.template import loader

# Create your views here.

def index(request):
    template = loader.get_template("webApp/index.html")
    context = {}
    return HttpResponse(template.render(context, request))