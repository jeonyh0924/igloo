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

    relation_users = models.ManyToManyField(
        'self',
        through='Relation',
        related_name='+',
        symmetrical=False,
    )

    @property
    def following(self):
        return Users.objects.filter(
            to_user_relation__from_user=self,
            to_user_retion__relation_type='f'
        )


class Relation(models.Model):
    CHOICE_RELATION_TYPE = (
        ('f', 'follow'),
        ('b', 'block'),
    )
    from_user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='from_user_relations',
        related_query_name='from_users_relation',
    )
    to_user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='to_user_relations',
        related_query_name='to_users_relation',
    )
    related_type = models.CharField(choices=CHOICE_RELATION_TYPE, max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('from_user', 'to_user')
        )
