from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'password',
            'introduce',
            'img_profile',
        )


class CheckUniqueIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username')

# User Create Selizer 와 User Update Serializer는 분리하여 만들도록 하자
# 회원가입에 필요한 속성과 회원정보 수정에 대한 속성은 다르기 때문이다.
