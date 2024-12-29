from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Post, Category
from .serializers import PostSerializer, CategorySerializer

from rest_framework.permissions import AllowAny

class PostListView(generics.ListAPIView):
    queryset = Post.objects.filter(status=1)  # Adjust the filter based on your requirements
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Allow anyone to access this view

class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.filter(status=1)
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]  # Allow anyone to access this view

class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        language = self.request.query_params.get('language', 'en')  # Default to 'en' if no language is provided
        return Category.objects.filter(language=language)