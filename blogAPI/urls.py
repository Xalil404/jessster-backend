from django.urls import path
from .views import PostListView, PostDetailView, CategoryListView, ToggleLikeView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('posts/<slug:slug>/like/', ToggleLikeView.as_view(), name='toggle-like'),
]
