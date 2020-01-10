from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.generics import get_object_or_404

from posts.models import Posts
from posts.permissions import IsOwnerOrReadOnly
from posts.serializer import PostSerializer, PostDetailSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )

    def get_object(self):
        return get_object_or_404(Posts, pk=self.kwargs.get("pk"))
