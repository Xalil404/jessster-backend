from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Video
from .serializers import VideoSerializer

# List all videos (view-only)
class VideoListView(generics.ListAPIView):
    serializer_class = VideoSerializer
    permission_classes = [permissions.AllowAny]  # Allow any user (authenticated or not)

    def get_queryset(self):
        lang = self.request.query_params.get('lang', 'en')  # Default to 'en' if 'lang' is not provided
        return Video.objects.filter(language=lang)


# Retrieve a single video (view-only)
class VideoDetailView(generics.RetrieveAPIView):
    serializer_class = VideoSerializer
    permission_classes = [permissions.AllowAny]  # Allow any user (authenticated or not)

    def get_queryset(self):
        lang = self.request.query_params.get('lang', 'en')  # Default to 'en' if 'lang' is not provided
        return Video.objects.filter(language=lang)

