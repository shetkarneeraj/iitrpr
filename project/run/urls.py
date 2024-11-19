from home.views import *
from django.urls import path
from home.institutes import *
from home.questions import *
from home.articles import *
from home.program import *
from home.programGroupMap import *
from home.views import *
from home.auth import UserRegistrationView, UserLoginView

urlpatterns = [
    path('index/', index),
    path('person/', People),
    path('institutes/', institutes),
    path('questions/', questions),
    path('articles/', articles),

    path('programs/', programsRoute),
    path('programgroups/', programGroupMap),

    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]