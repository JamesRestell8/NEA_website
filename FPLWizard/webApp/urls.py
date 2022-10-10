from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('allPlayers/', views.allPlayers, name='allPlayers'),
    path('MyFPL/', views.myFPL, name="MyFPL"),
    path('Positions/', views.positions, name='positions')
]
