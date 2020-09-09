from django.db import models

class News(models.Model):
    content = models.CharField(verbose_name="内容", max_length=500, null=True, blank=True)
    site = models.CharField(verbose_name="地点", max_length=100, null=True, blank=True)
    tag = models.CharField(verbose_name="标签", max_length=300, null=True, blank=True)
    like_count = models.IntegerField(verbose_name="点赞数", default=0)
    viewer_count = models.IntegerField(verbose_name="浏览数", default=0)
    comment_count = models.IntegerField(verbose_name="评论数", default=0)
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    user = models.ForeignKey(verbose_name="发布人", to='api.User', on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        db_table = 'news'


class NewsDetail(models.Model):
    key = models.CharField(verbose_name='腾讯云对象存储中的图片名(自定义的随机串)', max_length=255, help_text="用于以后删除对象存储文件")
    cos_url = models.CharField(verbose_name='腾讯云存储的图片路径', max_length=255)
    news = models.ForeignKey(verbose_name="动态", to='News', on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        db_table = 'newsdetail'


class Comment(models.Model):

    content = models.CharField(verbose_name='评论内容', max_length=255)
    reply = models.ForeignKey(verbose_name='回复的目标评论', to='self', related_name='replys', null=True,blank=True,on_delete=models.CASCADE)
    depth = models.IntegerField(verbose_name='评论层级(属于哪级评论)',default=1)
    root = models.ForeignKey(verbose_name='根(一级)评论的id', to='self', related_name='roots', null=True,blank=True,on_delete=models.CASCADE)
    like_count = models.IntegerField(verbose_name='点赞数',default=0)
    add_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)
    news = models.ForeignKey(verbose_name='动态', to='News', on_delete=models.CASCADE, db_constraint=False)
    user = models.ForeignKey(verbose_name="评论人", to='api.User', on_delete=models.CASCADE, db_constraint=False)
    # favor_count = models.IntegerField(verbose_name='评论点赞数', default=0)

    class Meta:
        db_table = 'comment'
