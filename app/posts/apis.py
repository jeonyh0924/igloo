# Create your views here.
from rest_framework import generics, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from posts.models import Posts
from posts.permissions import IsOwnerOrReadOnly
from posts.serializer import PostSerializer


class PostsView(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    # def list(self, request):
    #     query_set = self.get_queryset()
    #     serializer = PostSerializer(query_set, many=True)
    #     return Response(serializer.data)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )

    def get_object(self):
        return get_object_or_404(Posts, pk=self.kwargs.get("pk"))
#
