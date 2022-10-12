from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('MyFPL/', views.myFPL, name="MyFPL"),
    path('Positions/', views.positions, name='positions')
]
