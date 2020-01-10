from django.contrib.auth import get_user_model, authenticate
from rest_framework import generics, status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from members.serializers import UserSerializer, CheckUniqueIDSerializer

User = get_user_model()


class SignupView(generics.CreateAPIView):
    """
    username / password
    2개 필드 (pk 제외, 자동으로 생성)에 대한 값을 입력하여 POST요청
    필드값을 적절히 DB에 저장해 User Object 생성
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # method for creating password hashing relation
    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


# Check Username exists APIView
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


class UserProfileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class LogoutView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )
    """
    GET 요청으로 로그아웃 요청을 받는다
    해당 유저(request.user)가 가진 auth_token(Token object의 related_name)을 삭제
    """

    def delete(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
