# Generated by Django 2.1.15 on 2020-02-12 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='postPyeong',
            field=models.CharField(choices=[('1-7', '1-7평'), ('8-15', '8-15평'), ('16-25', '16-25평'), ('26-', '그 이상')], default='', max_length=10),
            preserve_default=False,
        ),
    ]
