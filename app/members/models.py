from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

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
        through='Relations',
        # 역방향 관계 무효
        related_name='+',
        # symmetrical // https://stackoverflow.com/questions/36852324/in-django-what-does-symmetrical-true-do
        symmetrical=False,
    )

    @property
    def follower(self):
        """
        나(request를 보낸 유저)를 팔로워 한 사람의 수
        """
        return Users.objects.filter(
            from_users_relation__to_user=self,
            from_users_relation__related_type='f'
        )

    @property
    def following(self):
        """
        내가 팔로우를 하는 사람들
        """
        return Users.objects.filter(
            to_user_relation__from_user=self,
            to_user_retion__relation_type='f'
        )

    @property
    def block_list(self):
        """
        내가 블록하는 유저 리스
        :return:
        """
        return Users.objects.filter(
            to_user_relations__from_user=self,
            to_user_relations__relation_type='b'
        )

    @property
    def follow(self, user):
        if not self.from_user_relations.filter(to_user=user).exists():
            self.from_user_relations.create(
                to_user=user,
                related_type='f',
            )
        return self.from_user_relations.get(to_user=user)

    @property
    def block(self, user):
        try:
            relation = self.from_user_relation.get(to_user=user)
            if relation.relation_type == 'f':
                relation.relation_type = 'b'
                relation.created_at = timezone.now()
                relation.save()
        except Relations.DoesNotExist:
            relation = self.from_user_relation.create(to_user=user, relation_type='b')
        return relation

    @property
    def follwer_relations(self):
        """
        :return: 나를 팔로우 하는 쿼리
        """
        return self.to_user_relations.filter(relation_type='f')

    @property
    def follwee_relations(self):
        """
        :return: 내가 팔로우 하는 쿼리
        """
        return self.from_user_relations.filter(relation_type='f')


class Relations(models.Model):
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

    # django meta options // https://docs.djangoproject.com/en/3.0/ref/models/options/