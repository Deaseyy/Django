# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-06-26 11:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid1', models.IntegerField()),
                ('uid2', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Swipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField(verbose_name='用户自身id')),
                ('sid', models.IntegerField(verbose_name='被滑的陌生人id')),
                ('mark', models.CharField(choices=[('like', 'like'), ('dislike', 'dislike'), ('superlike', 'superlike')], max_length=20, verbose_name='滑动类型')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='滑动的时间')),
            ],
        ),
    ]
