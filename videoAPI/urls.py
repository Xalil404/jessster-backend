from django.urls import path
from .views import VideoListView, VideoDetailView

urlpatterns = [
    path('videos/', VideoListView.as_view(), name='video-list'),  # To list and create videos
    path('videos/<int:pk>/', VideoDetailView.as_view(), name='video-detail'),  # To view, update, or delete a single video
]
