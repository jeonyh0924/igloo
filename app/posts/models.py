from django.conf import settings
from django.db import models


def get_image_filename(instance, filename):
    a = f'post_images/{instance.post.title}.svg'
    return a


def get_main_image_filename(instance, filename):
    a = f'post_images/{instance.title}_main.svg'
    return a


# Create your models here.
class Posts(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.TextField(
        '제목', max_length=50
    )
    content = models.TextField(
        '작성 글', max_length=500
    )
    main_image = models.ImageField(
        upload_to=get_main_image_filename,
        blank=True,
        null=True,
        verbose_name='메인 이미지',
    )
    pyeong = models.CharField(
        '평 수', max_length=20
    )
    created_at = models.DateTimeField(
        '생성 날짜', auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name='수정 날짜', auto_now=True, null=True, blank=True
    )

    like_users = models.ManyToManyField(
        'members.Users',
        through='PostLike',
        related_name='like_posts',
        related_query_name='like_post',
        blank=True,
        null=True,
    )

    colors = models.ManyToManyField(
        'posts.Colors',
        blank=True,
        null=True,
    )

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    class Meta:
        verbose_name = '게시글'
        verbose_name_plural = '게시글 목록'


class Comments(models.Model):
    post = models.ForeignKey(
        Posts,
        on_delete=models.CASCADE,
        verbose_name='포스트',
        related_name='comment_set',
        related_query_name='comments',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    content = models.TextField(
        '댓글 내용', max_length=500
    )
    # 글쓴이
    created_at = models.DateTimeField(
        '작성 날', auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        '수정 날짜', auto_now=True,
    )

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'

    def save(self, *args, **kwargs):
        # 여기서 이미지 처리를 하게 될 듯
        super().save(*args, **kwargs)


class PostLike(models.Model):
    post = models.ForeignKey(
        Posts,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        'members.Users',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return 'Post[{post_pk}] Like (User: {username})'.format(
            post_pk=self.post.pk,
            username=self.user.username,
        )

    class Meta:
        verbose_name = '게시글 좋아요'
        verbose_name_plural = f'{verbose_name} 목록'
        # 특정 유저가 특정 포스트 좋아요를 누른 정보는 유니크 해야 함.
        unique_together = (
            ('post', 'user'),
        )


class HousingTypes(models.Model):
    type = models.TextField(
        '주거 환경',
        max_length=20,
    )
    post = models.ForeignKey(
        Posts,
        on_delete=models.CASCADE,
    )


class Styles(models.Model):
    type = models.TextField(
        '디자인 스타일',
        max_length=10,
    )
    post = models.ForeignKey(
        Posts,
        on_delete=models.CASCADE,
    )


class Colors(models.Model):
    type = models.TextField(
        '색상',
        max_length=10
    )


class PostImages(models.Model):
    post = models.ForeignKey(
        Posts,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        upload_to=get_image_filename,
        verbose_name='다중 이미지',
    )
    image_comment = models.TextField(
        '사진 설명', max_length=200, blank=True, null=True,
    )
    # 이미지 추가 스택오버플로우 정보
    # https://stackoverflow.com/questions/34006994/how-to-upload-multiple-images-to-a-blog-post-in-django
