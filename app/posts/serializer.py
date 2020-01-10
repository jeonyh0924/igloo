from rest_framework import serializers

from posts.models import Posts


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = (
            'pk',
            'user',
            'title',
            'main_images',
        )


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta(PostSerializer):
        fields = PostSerializer.Meta.fields + (
            'pyeong',
            'colors',
        )
