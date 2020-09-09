# Generated by Django 2.2.3 on 2020-08-01 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(blank=True, max_length=500, null=True, verbose_name='内容')),
                ('site', models.CharField(blank=True, max_length=100, null=True, verbose_name='地点')),
                ('tag', models.CharField(blank=True, max_length=300, null=True, verbose_name='标签')),
                ('like_count', models.IntegerField(default=0, verbose_name='点赞数')),
                ('view_count', models.IntegerField(default=0, verbose_name='浏览数')),
                ('comment_count', models.IntegerField(default=0, verbose_name='评论数')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='api.User', verbose_name='发布人')),
            ],
            options={
                'db_table': 'news',
            },
        ),
        migrations.CreateModel(
            name='NewsDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(help_text='用于以后删除对象存储文件', max_length=255, verbose_name='腾讯云对象存储中的图片名(自定义的随机串)')),
                ('cos_url', models.CharField(max_length=255, verbose_name='腾讯云存储的图片路径')),
                ('news', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='circle.News', verbose_name='动态')),
            ],
            options={
                'db_table': 'newsdetail',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255, verbose_name='评论内容')),
                ('reply_id', models.IntegerField(default=None, verbose_name='回复的目标评论')),
                ('depth', models.IntegerField(default=1, verbose_name='评论深度(属于哪级评论)')),
                ('root_id', models.IntegerField(default=None, verbose_name='根(一级)评论的id')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('news', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='circle.News', verbose_name='动态')),
                ('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='api.User', verbose_name='评论人')),
            ],
            options={
                'db_table': 'comment',
            },
        ),
    ]
