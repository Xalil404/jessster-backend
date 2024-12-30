from django.shortcuts import render
from rest_framework import generics
from .models import Video
from .serializers import VideoSerializer

# List all videos (view-only)
class VideoListView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

# Retrieve a single video (view-only)
class VideoDetailView(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
