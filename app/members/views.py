import imghdr

import jwt
import requests
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.response import Response
# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from django.conf import settings

from config.settings.base import KAKAO_APP_ID, SECRET_KEY
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
    context = {
        'user': request.user
    }
    return render(request, 'login.html', context)


def facebook_login(request):
    api_base = 'https://graph.facebook.com/v3.2'
    api_get_access_token = f'{api_base}/oauth/access_token'
    api_me = f'{api_base}/me'

    # user = authenticate(request, facebook_request_token=request.GET.get('code'))
    code = request.GET.get('code')

    # request token을 access token으로 교환
    params = {
        'client_id': settings.FACEBOOK_APP_ID,
        'redirect_uri': 'http://localhost:8000/members/facebook-login/',
        'client_secret': settings.FACEBOOK_APP_SECRET,
        'code': code,
    }
    response = requests.get(api_get_access_token, params)
    # 인수로 전달한 문자열이 'JSON'형식일 것으로 생각
    # json.loads는 전달한 문자열이 JSON형식일 경우, 해당 문자열을 parsing해서 파이썬 Object를 리턴함
    # response_object = json.loads(response.text)
    data = response.json()
    access_token = data['access_token']
    params = {
        'access_token': access_token,
        'fields': ','.join([
            'id',
            'first_name',
            'last_name',
            'picture.type(large)',
        ])
    }
    response = requests.get(api_me, params)
    data = response.json()

    facebook_id = data['id']
    first_name = data['first_name']
    last_name = data['last_name']
    url_image = data['picture']['data']['url']
    # http get 요청의 응답을 받아와서, binary data 를 img_data 에 할당
    img_response = requests.get(url_image)
    img_data = img_response.content

    # 응답의 binary data를 사용해서, in-memory binary stream(file) 객체를 생성,
    # f = io.ByteIO(img_response.content)

    # FileField가 지원하는 InMemoryUploadedFile 객체를 사용하기,
    # imghdr 모듈을 사용해서 페이스북에서 받은 파일 확장자를 확인
    ext = imghdr.what('', h=img_data)
    f = SimpleUploadedFile(f'{facebook_id}.{ext}', img_response.content)

    jwt_token = jwt.encode({'username': facebook_id}, SECRET_KEY, algorithm='HS256').decode('utf-8')

    try:
        user = User.objects.get(username=facebook_id)
        user.last_name = last_name
        user.first_name = first_name
        user.save()
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=facebook_id,
            first_name=first_name,
            last_name=last_name,
            img_profile=f,
        )
    print(jwt_token)
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return HttpResponse(f'id: {facebook_id}, jwt: {jwt_token}')

    # return user
    #
    # if user:
    #     login(request, user)
    #     context = {
    #         'user': user,
    #     }
    #     return render(request, 'login.html', context)


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
    kakao_id = user_data['id']
    user_username = user_data['properties']['nickname']
    print(type(user_username))
    user_first_name = user_username[1:]
    user_last_name = user_username[0]

    kakao_user_image = user_data['properties']['profile_image']
    img_response = requests.get(kakao_user_image)
    img_data = img_response.content
    ext = imghdr.what('', h=img_data)
    f = SimpleUploadedFile(f'{kakao_id}.{ext}', img_response.content)

    jwt_token = jwt.encode({'id': kakao_id, 'username': kakao_id, }, SECRET_KEY, algorithm='HS256').decode('UTF-8')

    try:
        user = User.objects.get(username=kakao_id)
        first_name = user_first_name
        last_name = user_last_name
        user.save()
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=kakao_id,
            first_name=user_first_name,
            last_name=user_last_name,
            img_profile=f,
        )

    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    # return redirect('login-page')
    return HttpResponse(f'username: {kakao_id} token:{jwt_token}')
