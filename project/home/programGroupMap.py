from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from home.serializers import ProgramGroupMappingSerializer
from .models import ProgramGroupMapping

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def programGroupMap(request):
    # GET request: Fetch all ProgramGroupMapping records or a specific one by ID
    if request.method == 'GET':
        # If an ID is provided in the URL, retrieve the specific mapping, else all mappings
        if 'id' in request.query_params:
            try:
                program_group_mapping = ProgramGroupMapping.objects.get(pk=request.query_params['id'])
                serializer = ProgramGroupMappingSerializer(program_group_mapping)
                return Response(serializer.data)
            except ProgramGroupMapping.DoesNotExist:
                return Response({'error': 'ProgramGroupMapping not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            program_group_mappings = ProgramGroupMapping.objects.all()
            serializer = ProgramGroupMappingSerializer(program_group_mappings, many=True)
            return Response(serializer.data)

    # POST request: Create a new ProgramGroupMapping record
    elif request.method == 'POST':
        serializer = ProgramGroupMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT request: Update an existing ProgramGroupMapping record by ID
    elif request.method == 'PUT':
        if 'id' not in request.data:
            return Response({'error': 'ID is required for update'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            program_group_mapping = ProgramGroupMapping.objects.get(id=request.data['id'])
            serializer = ProgramGroupMappingSerializer(program_group_mapping, data=request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ProgramGroupMapping.DoesNotExist:
            return Response({'error': 'ProgramGroupMapping not found'}, status=status.HTTP_404_NOT_FOUND)

    # DELETE request: Delete a ProgramGroupMapping record by ID
    elif request.method == 'DELETE':
        if 'id' not in request.data:
            return Response({'error': 'ID is required for deletion'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            program_group_mapping = ProgramGroupMapping.objects.get(id=request.data['id'])
            program_group_mapping.delete()
            return Response({'message': 'ProgramGroupMapping deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except ProgramGroupMapping.DoesNotExist:
            return Response({'error': 'ProgramGroupMapping not found'}, status=status.HTTP_404_NOT_FOUND)
