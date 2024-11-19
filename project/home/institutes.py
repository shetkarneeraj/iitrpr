from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.serializers import InstitutionSerializer
from .models import Institution
from datetime import datetime

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def institutes(request):

    if request.method == 'GET':
        args = request.GET.get("search")
        if args:
            institutes = Institution.objects.filter(name__icontains=args)
            if not institutes:
                return Response({'error': 'Institution not found'})
        else:
            institutes = Institution.objects.all()
        serializer = InstitutionSerializer(institutes, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        institutes = Institution.objects.filter(name__icontains=request.data.get('name'))
        if institutes:
            return Response({'error': 'Institution already exists'})
        serializer = InstitutionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    if request.method == 'DELETE':
        institutes = Institution.objects.filter(name__icontains=request.data.get('name'))
        if not institutes:
            return Response({'error': 'Institution not found'})
        institutes.delete()
        return Response({'success': 'Institution deleted'})
    
    if request.method == 'PUT':
        institutes = Institution.objects.filter(name__icontains=request.data.get('name'))
        if not institutes:
            return Response({'error': 'Institution not found'})
        serializer = InstitutionSerializer(institutes[0], data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    