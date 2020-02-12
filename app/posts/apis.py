from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotAuthenticated, APIException
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from .models import Posts, PostLike, Comments, Colors, Pyeong
from .permissions import IsOwnerOrReadOnly, IsOwnerOrReadOnlyComment
from .serializer import PostSerializer, PostLikeSerializer, CommentSerializer, PostListSerializer


class PostsCreateView(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )


class PostListView(APIView):
    def get(self, request):
        posts = Posts.objects.all()
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostListSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )

    def get_object(self):
        return get_object_or_404(Posts, pk=self.kwargs.get("pk"))


class PostLikeCreate(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request, post_pk):
        # request.data.update(post=post_pk)
        post = get_object_or_404(Posts, pk=post_pk)
        serializer = PostLikeSerializer(
            data={**request.data, 'post': post_pk, }
        )
        if serializer.is_valid():
            if PostLike.objects.filter(
                    post=serializer.validated_data['post'],
                    user=request.user,
            ).exists():
                raise APIException('이미 좋아요 한 포스트 입니다.')
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_pk):
        post = get_object_or_404(Posts, pk=post_pk)
        post_like = get_object_or_404(PostLike, post=post, user=request.user)
        post_like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request, post_pk):
        post = get_object_or_404(Posts, pk=post_pk)
        serializer = CommentSerializer(
            data={**request.data, 'post': post_pk, 'author': request._user.pk, 'content': request.POST.get('content')}
        )
        if serializer.is_valid():
            serializer.save(post=post, author=request._user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentUpdateDelete(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrReadOnlyComment,
    )
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PostFiltering(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        colors = self.request.POST['colors']
        if colors is '':
            colors = Colors.objects.all()
        pyeong = self.request.POST['pyeong']
        if pyeong is None:
            pyeong = Pyeong.objects.all()
        housingtype = self.request.POST['housingtype']
        if housingtype is None:
            housingtype = Pyeong.objects.all()
        style = self.request.POST['style']
        return Posts.objects.filter(colors=colors,
                                    pyeong=pyeong,
                                    housingtype=housingtype,
                                    style=style
                                    )
