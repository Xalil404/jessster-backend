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

from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


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








class ToggleLikeView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is logged in

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug, status=1)
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)  # Unlike the post
            liked = False
        else:
            post.likes.add(user)  # Like the post
            liked = True

        return Response({
            'liked': liked,
            'likes_count': post.likes.count(),
        })
