# Generated by Django 2.1.15 on 2019-12-27 17:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import posts.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Colors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField(max_length=10, verbose_name='색상')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=500, verbose_name='댓글 내용')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='작성 날')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 날짜')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '댓글',
                'verbose_name_plural': '댓글 목록',
            },
        ),
        migrations.CreateModel(
            name='HousingTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField(max_length=20, verbose_name='주거 환경')),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=posts.models.get_image_filename, verbose_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='Postlikes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '게시글 좋아요',
                'verbose_name_plural': '게시글 좋아요 목록',
            },
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=50, verbose_name='제목')),
                ('content', models.TextField(max_length=500, verbose_name='작성 글')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 날짜')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='수정 날짜')),
                ('colors', models.ManyToManyField(to='posts.Colors')),
                ('like_users', models.ManyToManyField(related_name='like_posts', related_query_name='like_post', through='posts.Postlikes', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Styles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField(max_length=10, verbose_name='디자인 스타일')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Posts')),
            ],
        ),
        migrations.AddField(
            model_name='postlikes',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Posts'),
        ),
        migrations.AddField(
            model_name='postlikes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='images',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Posts'),
        ),
        migrations.AddField(
            model_name='housingtypes',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Posts'),
        ),
        migrations.AddField(
            model_name='comments',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_set', related_query_name='comments', to='posts.Posts', verbose_name='포스트'),
        ),
        migrations.AlterUniqueTogether(
            name='postlikes',
            unique_together={('post', 'user')},
        ),
    ]
