from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('MyFPL/', views.myFPL, name="MyFPL"),
    path('Positions/', views.positions, name='positions'),
    path('Goalkeepers/', views.goalkeepers, name='goalkeepers'),
    path('Defenders/', views.defenders, name='defenders'),
    path('Midfielders/', views.midfielders, name='midfielders'),
    path('Attackers/', views.attackers, name='attackers'),
    path('MyFPL/fplIDHelp/', views.fplIDHelp, name='fplIDHelp'),
    path('TeamRankings/', views.teamStrength, name="teamStrength")
]
