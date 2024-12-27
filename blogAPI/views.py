from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Post, Category
from .serializers import PostSerializer, CategorySerializer

class PostListView(generics.ListAPIView):
    queryset = Post.objects.filter(status=1)
    serializer_class = PostSerializer

class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.filter(status=1)
    serializer_class = PostSerializer

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
