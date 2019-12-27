from django.contrib.auth.models import AbstractUser
from django.db import models

UserChoice = (
    ('common', 'common'),
    ('designer', 'designer'),
)


# Create your models here.
class Users(AbstractUser):
    img_profile = models.ImageField(
        '프로필 이미지', upload_to='user', blank=True,
    )
    introduce = models.TextField(
        '소개', blank=True,
    )
    user_type = models.CharField(
        '유저 타입', choices=UserChoice, max_length=100,
    )
