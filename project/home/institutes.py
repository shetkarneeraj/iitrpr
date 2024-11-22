from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.serializers import InstitutionSerializer
from .models import Institution
from datetime import datetime
from rest_framework import status

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def institutes(request):
    # GET request: Accessible to all users

    if not user.is_authenticated:
        return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        args = request.GET.get("search")
        if args:
            institutes = Institution.objects.filter(name__icontains=args)
            if not institutes:
                return Response({'error': 'Institution not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            institutes = Institution.objects.all()
        serializer = InstitutionSerializer(institutes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Role validation for restricted methods
    user = request.user
    if not user.is_authenticated or getattr(user, "role", None) != "superadmin":
        return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

    # POST request: Create a new institution
    if request.method == 'POST':
        institutes = Institution.objects.filter(name__icontains=request.data.get('name'))
        if institutes.exists():
            return Response({'error': 'Institution already exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = InstitutionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE request: Delete an institution by name
    elif request.method == 'DELETE':
        institutes = Institution.objects.filter(name__icontains=request.data.get('name'))
        if not institutes:
            return Response({'error': 'Institution not found'}, status=status.HTTP_404_NOT_FOUND)
        institutes.delete()
        return Response({'success': 'Institution deleted'}, status=status.HTTP_204_NO_CONTENT)

    # PUT request: Update an existing institution by name
    elif request.method == 'PUT':
        institutes = Institution.objects.filter(name__icontains=request.data.get('name'))
        if not institutes:
            return Response({'error': 'Institution not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = InstitutionSerializer(institutes[0], data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)