from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Post, Category, Comment
from .serializers import PostSerializer, CategorySerializer, CommentSerializer

from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from django.db.models import Count, F

from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Default queryset filters (all published posts)
        queryset = Post.objects.filter(status=1)

        # Check for sorting criteria passed as query params
        sort_by = self.request.query_params.get('sort_by', 'created_on')  # Default to created_on
        order = self.request.query_params.get('order', 'desc')  # Default to descending order

        # Filter by category if the 'category' query parameter is provided
        category_slug = self.request.query_params.get('category', None)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Filter by language if the 'language' query parameter is provided
        language = self.request.query_params.get('language', None)
        if language:
            queryset = queryset.filter(language=language)

        # Handle sorting by views, likes, comments, or created date
        if sort_by == 'views':
            queryset = queryset.order_by(F('number_of_views').desc() if order == 'desc' else F('number_of_views').asc())
        elif sort_by == 'likes':
            queryset = queryset.annotate(likes_count=Count('likes')).order_by(F('likes_count').desc() if order == 'desc' else F('likes_count').asc())
        elif sort_by == 'comments':
            queryset = queryset.annotate(num_comments=Count('comments')).order_by(F('num_comments').desc() if order == 'desc' else F('num_comments').asc())
        else:
            # Default to ordering by creation date
            queryset = queryset.order_by(F('created_on').desc() if order == 'desc' else F('created_on').asc())

        return queryset

'''
class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Default queryset filters
        queryset = Post.objects.filter(status=1)
        
        # Check for sorting criteria passed as query params
        sort_by = self.request.query_params.get('sort_by', 'created_on')  # Default to created_on
        order = self.request.query_params.get('order', 'desc')  # Default to descending order
        
        # Filter by category if the 'category' query parameter is provided
        category_slug = self.request.query_params.get('category', None)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Filter by language if the 'language' query parameter is provided
        language = self.request.query_params.get('language', 'en')  # Default to 'en' if no language is provided
        queryset = queryset.filter(language=language)
        
        if sort_by == 'views':
            queryset = queryset.order_by(F('number_of_views').desc() if order == 'desc' else F('number_of_views').asc())
        elif sort_by == 'likes':
            queryset = queryset.annotate(likes_count=Count('likes')).order_by(F('likes_count').desc() if order == 'desc' else F('likes_count').asc())
        elif sort_by == 'comments':
            queryset = queryset.annotate(num_comments=Count('comments')).order_by(F('num_comments').desc() if order == 'desc' else F('num_comments').asc())
        else:
            # Default to ordering by creation date
            queryset = queryset.order_by(F('created_on').desc() if order == 'desc' else F('created_on').asc())
        
        return queryset
        '''



class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.filter(status=1)
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]  # Allow anyone to access this view

    def get_object(self):
        post = super().get_object()
        post.increment_views()  # Increment views using the model's method
        return post
    
    def get_serializer_context(self):
        # Pass the request object to the serializer's context
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


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


# Add a view for Comment Creation
class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_slug = self.kwargs['slug']  # Retrieve the slug from URL parameters
        post = get_object_or_404(Post, slug=post_slug)
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        post_slug = self.kwargs['slug']
        post = get_object_or_404(Post, slug=post_slug)
        serializer.save(user=self.request.user, post=post)


# Add a view for retrieving a single comment (optional)
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Comment.objects.filter(post__slug=self.kwargs['slug'])



# Search posts 
@api_view(['GET'])
@permission_classes([AllowAny])  # Allow anonymous users to access this view
def search_posts(request):
    query = request.GET.get('q', '')
    if query:
        posts = Post.objects.filter(
            (Q(title__icontains=query) | Q(content__icontains=query)),
            status=1
        )
        serializer = PostSerializer(posts, many=True)
        return Response({"results": serializer.data})
    else:
        return Response({"results": []})


# Retrieve the list of articles a user liked
class LikedArticlesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        liked_posts = Post.objects.filter(likes=user, status=1)  # Filter only published posts
        serializer = PostSerializer(liked_posts, many=True)
        return Response(serializer.data)



# to show limited articles on the home page quickly rather than fetching all articles
class LimitedPostListView(PostListView):
    def get_queryset(self):
        queryset = super().get_queryset()

        # Optional language filter
        language = self.request.query_params.get('language', None)
        if language:
            queryset = queryset.filter(language=language)

        # Limit to 13 latest articles
        return queryset[:13]


# Fetch the 4 most viewed articles to not filter on the front end so home page loads faster
class MostViewedPostsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # Get the language from query params (defaults to 'en' if not provided)
        language = request.query_params.get('language', 'en')  # Default to 'en'

        # Fetch the top 4 most viewed posts in the specified language
        posts = Post.objects.filter(language=language, status=1).order_by('-number_of_views')[:4]

        # Serialize the data into a simple list of dictionaries
        posts_data = [
            {
                'id': post.id,
                'slug': post.slug,
                'title': post.title,
                'featured_image': post.featured_image.url if post.featured_image else None
            }
            for post in posts
        ]

        # Return the posts as JSON response
        return JsonResponse(posts_data, safe=False)
