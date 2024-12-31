from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Post, Category
from .serializers import PostSerializer, CategorySerializer

from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status


class PostListView(generics.ListAPIView):
    queryset = Post.objects.filter(status=1)  # Adjust the filter based on your requirements
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Allow anyone to access this view

class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.filter(status=1)
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]  # Allow anyone to access this view

    def get_object(self):
        post = super().get_object()
        post.increment_views()  # Increment views using the model's method
        return post

class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        language = self.request.query_params.get('language', 'en')  # Default to 'en' if no language is provided
        return Category.objects.filter(language=language)




@api_view(['POST'])
def increment_views(request, slug):
    """
    Increment views count for a specific post.
    """
    try:
        post = Post.objects.get(slug=slug)
        post.increment_views()  # Use the model's method to increment views
        return Response({'message': 'Views incremented successfully', 'number_of_views': post.number_of_views}, status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)




@api_view(['POST'])
def increment_likes(request, slug):
    """
    Increment likes count for a specific post.
    """
    try:
        post = Post.objects.get(slug=slug)
        post.likes += 1
        post.save()
        return Response({'message': 'Likes incremented successfully', 'likes': post.likes}, status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

