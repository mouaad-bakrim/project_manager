from django.contrib import admin
from django.urls import path
from . import views
from .views import generate_project, dashboard

urlpatterns = [
    path('', generate_project, name='generer_projet'),
    path('dashboard/', dashboard, name='dashboard'),
]
