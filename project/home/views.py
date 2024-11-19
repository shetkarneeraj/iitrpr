from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.serializers import PersonSerializer
from django.shortcuts import render, redirect
from .models import Person
from datetime import datetime


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
def People(request):

    if request.method == 'GET':
        args = request.GET.get("search")
        # Get data from Person using keyword search
        people = Person.objects.filter(name__icontains=args)
        serializer = PersonSerializer(people, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
@api_view(['GET', 'POST'])
def logout_view(request):
    return Response({'message': 'Logged out successfully.'})