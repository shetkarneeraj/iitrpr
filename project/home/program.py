from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.serializers import ProgramSerializer, ProgramGroupMappingSerializer, GroupSerializer
from .models import Program, ProgramGroupMapping, Group
from datetime import datetime

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def programsRoute(request):

    if request.method == 'GET':
        args = request.GET.get("search")
        if args:
            programs = Program.objects.filter(name__icontains=args)
            if not programs:
                return Response({'error': 'Program not found'})
        else:
            programs = Program.objects.all()
        serializer = ProgramSerializer(programs, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        programs = Program.objects.filter(name=request.data.get('name'))
        if programs:
            return Response({'error': 'Program already exists'})
        serializer = ProgramSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    if request.method == 'DELETE':
        programs = Program.objects.filter(name=request.data.get('name'))
        if not programs:
            return Response({'error': 'Program not found'})
        programs.delete()
        return Response({'success': 'Program deleted'})
    
    if request.method == 'PUT':
        programs = Program.objects.filter(name=request.data.get('name'))
        if not programs:
            return Response({'error': 'Program not found'})
        serializer = ProgramSerializer(programs[0], data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)