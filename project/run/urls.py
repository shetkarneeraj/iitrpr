from home.views import *
from django.urls import path
from home.institutes import *
from home.questions import *
from home.articles import *

urlpatterns = [
    path('index/', index),
    path('person/', People),
    path('institutes/', institutes),
    path('questions/', questions),
    path('articles/', articles),
]