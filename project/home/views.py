from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, redirect
from datetime import datetime
from rest_framework.authtoken.models import Token


# Create your views here.
@api_view(['GET', 'POST'])
def index(request):

    if request.method == 'GET':
        return render(request, 'home.html')
    
    if request.method == 'POST':
        course = request.data.get('course') # Data in the json request body
        courses = {
            'courses': ['Python', 'Django', 'JavaScript', 'React', 'Data Science'] + [course]
        }
        return Response(courses)
    
@api_view(['GET', 'POST'])
def logout_view(request):
    return Response({'message': 'Logged out successfully.'})