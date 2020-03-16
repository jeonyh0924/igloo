import imghdr
import requests
from django.contrib.auth import get_user_model, login, authenticate
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.response import Response
# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView

from config import settings
from .models import Users
from .serializers import UserProfileSerializer, ChangePasswordSerializer
from .permissions import IsOwnerOrReadOnly

User = get_user_model()


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
        'client_id': 'c5fe0d7cf28e7714d8f01200f604a03b',
        'redirect_url': 'http://localhost:8000/members/kakao-login/',
        'code': kakao_access_code
    }
    kakao_reponse = requests.post(url, headers=headers, data=body)
    #  front 에서 받아야 할 역할 완료 / 
    return HttpResponse(kakao_reponse.text)
