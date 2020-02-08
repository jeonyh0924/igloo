from rest_framework import serializers
from .models import Posts, PostImages, PostLike, Comments
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'img_profile',
            'introduce',
            'user_type',

        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = (
            'image',
        )


class PostSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    images = PostImageSerializer(source='postimages_set', many=True, read_only=True)
    comment = CommentSerializer(source='comment_set', many=True)

    class Meta:
        model = Posts
        fields = (
            'id',
            'user',
            'title',
            'content',
            'main_image',
            'pyeong',
            'images',
            'comment',
        )

    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES
        user = self.context.get("request").user
        validated_data["user"] = user
        post = super().create(validated_data)
        for image_data in images_data.values():
            PostImages.objects.create(
                post=post,
                image=image_data,
            )
        return post


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = (
            'post',
            'user',
        )
        read_only_fields = (
            'user',
        )


class PostLikeListSerializer(serializers.ModelSerializer):
    posts = PostSerializer(source='post')

    class Meta:
        model = PostLike
        fields = (
            'posts',
        )
