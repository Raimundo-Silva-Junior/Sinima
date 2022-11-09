from django.urls import path
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView,
    PostUpdateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
    )
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('filmes/', UserPostListView.as_view(), name='blog-filmes'),
    path('series/', UserPostListView.as_view(), name='blog-series'),
    path('animes/', UserPostListView.as_view(), name='blog-animes'),
    path('user/<str:username>/', UserPostListView.as_view(), name='blog-user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='blog-post-detail'),
    path('post/new/', PostCreateView.as_view(), name='blog-post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='blog-post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='blog-post-delete'),
]