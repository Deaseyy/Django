# Generated by Django 2.0.7 on 2019-05-07 06:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=10, unique=True, verbose_name='账号')),
                ('password', models.CharField(max_length=255, verbose_name='密码')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('operate_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('icon', models.ImageField(null=True, upload_to='upload')),
            ],
            options={
                'db_table': 'my_user',
            },
        ),
        migrations.CreateModel(
            name='MyUserToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=100, unique=True, verbose_name='token标识符')),
                ('out_time', models.DateTimeField(null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.MyUser')),
            ],
            options={
                'db_table': 'my_token',
            },
        ),
    ]
