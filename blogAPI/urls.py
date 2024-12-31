from django.urls import path
from .views import PostListView, PostDetailView, CategoryListView, increment_views, increment_likes

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('posts/<slug:slug>/increment-views/', increment_views, name='increment-views'),  # Views URL
    path('posts/<slug:slug>/increment-likes/', increment_likes, name='increment-likes'),  # Likes URL
]
