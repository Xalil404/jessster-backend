from django.urls import path
from .views import PostListView, PostDetailView, CategoryListView, ToggleLikeView, CommentListView, CommentDetailView, LikedArticlesView, LimitedPostListView, MostViewedPostsView
from . import views

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('posts/<slug:slug>/like/', ToggleLikeView.as_view(), name='toggle-like'),
    path('posts/<slug:slug>/comments/', CommentListView.as_view(), name='comment-list'),
    path('posts/<slug:slug>/comments/<int:id>/', CommentDetailView.as_view(), name='comment-detail'),
    path('search/', views.search_posts, name='search_posts'),
    path('user/liked-articles/', LikedArticlesView.as_view(), name='liked-articles'),
    path('articles/limited/', LimitedPostListView.as_view(), name='limited-post-list'),
    path('articles/most-viewed/', MostViewedPostsView.as_view(), name='most_viewed_posts'),
]
