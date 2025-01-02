from django.urls import path
from .views import PostListView, PostDetailView, CategoryListView, ToggleLikeView, CommentListView, CommentDetailView
from . import views

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('posts/<slug:slug>/like/', ToggleLikeView.as_view(), name='toggle-like'),
    path('posts/<slug:slug>/comments/', CommentListView.as_view(), name='comment-list'),
    path('posts/<slug:slug>/comments/<int:id>/', CommentDetailView.as_view(), name='comment-detail'),
    path('search/', views.search_posts, name='search_posts'),
]
