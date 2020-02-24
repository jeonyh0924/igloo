from rest_framework import serializers
from rest_framework.relations import StringRelatedField
from .models import Posts, PostImages, PostLike, Comments, Pyeong, Colors, HousingTypes, Styles
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
        fields = (
            'author',
            'content',
            'created_at',
            'updated_at',
        )


class PyeongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pyeong
        fields = (
            'type',
        )


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colors
        fields = (
            'type',
        )


class HousingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HousingTypes
        fields = (
            'type',
        )


class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Styles
        fields = (
            'type',
        )


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = (
            'image',
        )


class PostSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    images = PostImageSerializer(source='postimages_set', many=True, read_only=True)
    pyeong = StringRelatedField(many=True, read_only=True)
    colors = StringRelatedField(many=True, read_only=True)
    housingtype = StringRelatedField(many=True, read_only=True, )
    style = StringRelatedField(many=True, read_only=True, )

    class Meta:
        model = Posts
        fields = (
            'id',
            'user',
            'title',
            'content',
            'main_image',
            'images',
            'pyeong',
            'colors',
            'housingtype',
            'style',

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


class PostListSerializer(PostSerializer):
    comment = CommentSerializer(source='comment_set', many=True)
    pyeong = PyeongSerializer(many=True, allow_null=True, read_only=True)
    colors = ColorSerializer(many=True, read_only=True, allow_null=True)
    housingtype = HousingTypeSerializer(many=True, read_only=True)
    style = StyleSerializer(many=True, read_only=True)

    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + (
            'pyeong',
            'colors',
            'housingtype',
            'style',
            'comment',
        )


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = (
            'post',
            'user',
        )


class PostLikeListSerializer(serializers.ModelSerializer):
    posts = PostListSerializer(source='post')

    class Meta:
        model = PostLike
        fields = (
            'posts',
        )
