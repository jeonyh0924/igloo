import imghdr

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


class FacebookBackend:
    api_base = 'https://graph.facebook.com/v3.2'
    api_get_access_token = f'{api_base}/oauth/access_token'
    api_me = f'{api_base}/me'

    def get_user_by_access_token(self, access_token):
        params = {
            'access_token': access_token,
            'fields': ','.join([
                'id',
                'first_name',
                'last_name',
                'picture.type(large)',
            ])
        }
        response = requests.get(self.api_me, params)
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
        return user

    def authenticate(self, request, facebook_request_token):
        # 페이스북으로부터 받아온 request token
        code = facebook_request_token

        # request token을 access token으로 교환
        params = {
            'client_id': settings.FACEBOOK_APP_ID,
            'redirect_uri': 'http://localhost:8000/members/facebook-login/',
            'client_secret': settings.FACEBOOK_APP_SECRET,
            'code': code,
        }
        response = requests.get(self.api_get_access_token, params)
        # 인수로 전달한 문자열이 'JSON'형식일 것으로 생각
        # json.loads는 전달한 문자열이 JSON형식일 경우, 해당 문자열을 parsing해서 파이썬 Object를 리턴함
        # response_object = json.loads(response.text)
        data = response.json()
        access_token = data['access_token']
        self.get_user_by_access_token(access_token)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
