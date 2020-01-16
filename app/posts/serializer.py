from rest_framework import serializers

from members.serializers import UserSerializer
from .models import Posts, PostImages


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = (
            'image',
        )


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    images = PostImageSerializer(source='postimages_set', many=True, read_only=True)

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
