from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from home.serializers import ChapterSerializer
from .models import Chapter
from datetime import datetime

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def chapters(request):

    # GET request: Fetch chapters based on a search query or return all chapters
    if request.method == 'GET':
        args = request.GET.get("search")
        if args:
            chapters = Chapter.objects.filter(title__icontains=args)
            if not chapters:
                return Response({'error': 'Chapter not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            chapters = Chapter.objects.all()
        serializer = ChapterSerializer(chapters, many=True)
        return Response(serializer.data)

    # POST request: Create a new chapter
    elif request.method == 'POST':
        existing_chapter = Chapter.objects.filter(title__icontains=request.data.get('title'))
        if existing_chapter.exists():
            return Response({'error': 'Chapter already exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ChapterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE request: Delete a chapter by its title
    elif request.method == 'DELETE':
        chapter_title = request.data.get('title')
        if not chapter_title:
            return Response({'error': 'Title is required for deletion'}, status=status.HTTP_400_BAD_REQUEST)

        chapter = Chapter.objects.filter(title__icontains=chapter_title).first()
        if not chapter:
            return Response({'error': 'Chapter not found'}, status=status.HTTP_404_NOT_FOUND)

        chapter.delete()
        return Response({'success': 'Chapter deleted'}, status=status.HTTP_204_NO_CONTENT)

    # PUT request: Update an existing chapter by its title
    elif request.method == 'PUT':
        chapter_title = request.data.get('title')
        if not chapter_title:
            return Response({'error': 'Title is required for update'}, status=status.HTTP_400_BAD_REQUEST)

        chapter = Chapter.objects.filter(title__icontains=chapter_title).first()
        if not chapter:
            return Response({'error': 'Chapter not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChapterSerializer(chapter, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
