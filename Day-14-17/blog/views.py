from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Post, Comment
from .serializers import AuthorSerializer, PostSerializer, CommentSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email']

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_published', 'author'] # Exact match filtering
    search_fields = ['title', 'content']          # Text search
    ordering_fields = ['created_at', 'title']     # Sorting

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post']