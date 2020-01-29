from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.serializer import PostImageSerializer, PostSerializer

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


class UserProfileSerializer(serializers.ModelSerializer):
    # relation_users = serializers.StringRelatedField(many=True, read_only=True)

    relation_users = serializers.StringRelatedField(many=True)
    count_followers = serializers.SerializerMethodField(read_only=True)

    def get_count_followers(self, user):
        return user.follower.count()

    class Meta:
        model = User
        fields = (
            'pk',
            'relation_users',
            'count_followers',
            'username',
            'img_profile',
            'introduce',
            'user_type',

        )


class UserProfileChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'img_profile',
            'introduce',
        )


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class CheckUniqueIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
        )


class UserPostsSerializer(CheckUniqueIDSerializer):
    posts = PostSerializer(source='posts_set', many=True, read_only=True)

    class Meta(CheckUniqueIDSerializer.Meta):
        fields = CheckUniqueIDSerializer.Meta.fields + (
            'posts',
        )
# User Create Selizer 와 User Update Serializer는 분리하여 만들도록 하자
# 회원가입에 필요한 속성과 회원정보 수정에 대한 속성은 다르기 때문이다.
