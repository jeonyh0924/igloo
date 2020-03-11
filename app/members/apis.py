from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from rest_framework import generics, status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from members.models import Relations
from members.permissions import IsOwnerOrReadOnly
from posts.models import PostLike
from posts.serializer import PostSerializer, PostLikeListSerializer, PostLikeSerializer
from .serializers import UserSerializer, CheckUniqueIDSerializer, UserProfileSerializer, UserProfileChangeSerializer, \
    UserPostsSerializer

User = get_user_model()


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


class CheckUniqueIDView(APIView):
    def post(self, request):
        # response = {}
        serializer = CheckUniqueIDSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(username=serializer.data['username'])
            if not user.exists():
                return Response({"username": serializer.data['username'], "message": '사용 가능한 아이디입니다.'},
                                status=status.HTTP_200_OK)
        else:
            return Response({"message": '해당 사용자 이름은 이미 존재합니다.'}, status=status.HTTP_400_BAD_REQUEST)


class AuthTokenView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, __ = Token.objects.get_or_create(user=user)
            data = {
                # 데이터의 형태로 담아서 보내준다.
                'token': token.key,
            }
            return Response(data)
        raise AuthenticationFailed()


class FacebookAuthTokenView(APIView):
    def post(self, request):
        """
        전달받은 토큰 값( facebook access token key)과 유저 정보(token, user)를 사용해서
        정상적인 토큰인지 확인 후
        디비에 해당하는 유저가 존재하는지 검사, 있다면 토큰을 주고, 없다면 유저 생성 후 토큰을 발급한다.
        """
        pass

    pass


class UserProfileView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class LogoutView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def delete(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class FollowUserView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    )

    def post(self, request):
        user = request._user
        other_pk = request.data.get('other_pk')
        other_user = get_object_or_404(User, pk=other_pk)

        relation = user.from_user_relations.get(to_user=other_user)
        if not relation:
            # if relation.related_type == 'f':
            user.from_user_relations.create(
                to_user=other_user,
                related_type='f',
            )
            return Response({"message": "follow User 가 되었습니다."}, status=status.HTTP_201_CREATED)
        elif relation.related_type == 'b':
            relation.related_type = 'f'
            relation.created_at = timezone.now()
            relation.save()
            return Response({"message": "follow User로 변경 되었습니다."}, status=status.HTTP_200_OK)
        elif relation.related_type == 'f':
            return Response({"message": "이미 존재하는 follow 입니다."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request._user
        other_pk = request.data.get('other_pk')
        other_user = get_object_or_404(User, pk=other_pk)
        try:
            relation = user.from_user_relations.get(to_user=other_user)
            if relation.related_type == 'f':
                relation.related_type = 'b'
                relation.created_at = timezone.now()
                relation.save()
            else:
                return Response({'message': '이미 Block 상태의 유저이거나 유저의 pk가 올바르지 않습니다.'},
                                status=status.HTTP_400_BAD_REQUEST)
        except Relations.DoesNotExist:
            user.from_user_relation.create(to_user=other_user, related_type='b')
        return Response({'message': 'Block User로 변경되었습니다.'}, status=status.HTTP_200_OK)


class FollowerView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request):
        user = request._user
        follower_user = user.follower
        serializer = CheckUniqueIDSerializer(follower_user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowingView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request):
        user = request._user
        following_user = user.following
        serializer = UserPostsSerializer(following_user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyProfileView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    )

    def get(self, request):
        user = request._user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request._user
        serializer = UserProfileChangeSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostLIkeListView(APIView):
    permissions = (
        permissions.IsAuthenticated,
    )

    def get(self, request):
        user = request._user
        post_list = user.postlike_set.all()
        serializer = PostLikeListSerializer(post_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
