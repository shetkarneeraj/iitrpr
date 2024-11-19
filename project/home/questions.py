from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from home.serializers import QuestionSerializer
from .models import Question
from datetime import datetime

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def questions(request):

    if request.method == 'POST':
        data = request.data
        serializer = QuestionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    