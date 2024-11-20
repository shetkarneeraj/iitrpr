from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from home.serializers import VideoSerializer
from .models import Video

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def videos(request):

    # GET request: Fetch videos based on a search query or return all videos
    if request.method == 'GET':
        args = request.GET.get("search")
        if args:
            videos = Video.objects.filter(title__icontains=args)
            if not videos:
                return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

    # POST request: Create a new video
    elif request.method == 'POST':
        existing_video = Video.objects.filter(link__icontains=request.data.get('link'))
        if existing_video.exists():
            return Response({'error': 'Video already exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE request: Delete a video by its title
    elif request.method == 'DELETE':
        video_title = request.data.get('title')
        if not video_title:
            return Response({'error': 'Title is required for deletion'}, status=status.HTTP_400_BAD_REQUEST)

        video = Video.objects.filter(title__icontains=video_title).first()
        if not video:
            return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

        video.delete()
        return Response({'success': 'Video deleted'}, status=status.HTTP_204_NO_CONTENT)

    # PUT request: Update an existing video by its title
    elif request.method == 'PUT':
        video_title = request.data.get('title')
        if not video_title:
            return Response({'error': 'Title is required for update'}, status=status.HTTP_400_BAD_REQUEST)

        video = Video.objects.filter(title__icontains=video_title).first()
        if not video:
            return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = VideoSerializer(video, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
