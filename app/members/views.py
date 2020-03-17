import imghdr
import requests
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.response import Response
# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView

from config import settings
from config.settings.base import KAKAO_APP_ID
from .models import Users
from .serializers import UserProfileSerializer, ChangePasswordSerializer
from .permissions import IsOwnerOrReadOnly

User = get_user_model()


def user_logout(request):
    logout(request)
    return redirect('login-page')


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list와 detail 기능 자동 지원
    """
    queryset = Users.objects.all()
    serializer_class = UserProfileSerializer


class UserModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet 은 'list', 'create', 'retrieve', 'update', 'destroy' 기능을 지원한다.
    """
    queryset = Users.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )


class UpdatePassword(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def facebook_login_page(request):
    return render(request, 'login.html')


def facebook_login(request):
    user = authenticate(request, facebook_request_token=request.GET.get('code'))
    if user:
        login(request, user)
        context = {
            'user': user,
        }
        return render(request, 'login.html', context)
    return Response(status=status.HTTP_400_BAD_REQUEST)


def kakao_login(request):
    kakao_access_code = request.GET.get('code')
    url = 'https://kauth.kakao.com/oauth/token'
    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    body = {
        'grant_type': 'authorization_code',
        'client_id': KAKAO_APP_ID,
        'redirect_url': 'http://localhost:8000/members/kakao-login/',
        'code': kakao_access_code
    }
    kakao_reponse = requests.post(url, headers=headers, data=body)
    #  front 에서 받아야 할 역할 완료 /
    data = kakao_reponse.json()
    access_token = data['access_token']

    url = 'https://kapi.kakao.com/v2/user/me'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    kakao_response = requests.post(url, headers=headers)

    user_data = kakao_response.json()
    kakao_user_id = user_data['id']
    user_username = user_data['properties']['nickname']
    print(type(user_username))
    user_first_name = user_username[0]
    user_last_name = user_username[1:]

    kakao_user_image = user_data['properties']['profile_image']
    img_response = requests.get(kakao_user_image)
    img_data = img_response.content
    ext = imghdr.what('', h=img_data)
    f = SimpleUploadedFile(f'{kakao_user_id}.{ext}', img_response.content)

    try:
        user = User.objects.get(username=kakao_user_id)
        first_name = user_first_name
        last_name = user_last_name
        user.save()
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=kakao_user_id,
            first_name=user_first_name,
            last_name=user_last_name,
            img_profile=f,
        )

    return HttpResponse(user)
