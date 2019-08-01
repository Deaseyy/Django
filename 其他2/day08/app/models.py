from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=20, unique=True, null=False)
    desc = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    # is_show, 发布状态
    is_show = models.BooleanField(default=1)

    class Meta:
        db_table = 'article'

