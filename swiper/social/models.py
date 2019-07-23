from django.db import models

# Create your models here.

class Swipe(models.Model):
    MARK = (
        ('like', 'like'),
        ('dislike', 'dislike'),
        ('superlike', 'superlike')
    )
    uid = models.IntegerField(verbose_name='用户自身id')

    sid = models.IntegerField(verbose_name='被滑的陌生人id')

    mark = models.CharField(max_length=20, choices=MARK, verbose_name='滑动类型')

    time = models.DateTimeField(auto_now_add=True, verbose_name='滑动的时间')

    # 喜欢
    @classmethod
    def like(cls, uid, sid):
        return Swipe.objects.create(uid=uid, sid=sid, mark='like')

    # 是否也喜欢我
    @classmethod
    def has_like_me(cls, uid, sid):
        return Swipe.objects.filter(uid=uid, sid=sid, mark__in=['like', 'superlike']).exists()

    #不喜欢
    @classmethod
    def dislike(cls, uid, sid):
        return Swipe.objects.create(uid=uid, sid=sid, mark='dislike')

    #超级喜欢
    @classmethod
    def superlike(cls, uid, sid):
        return Swipe.objects.create(uid=uid, sid=sid, mark='superlike')


class Friend(models.Model):
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()

    # 添加好友关系
    @classmethod
    def make_friends(cls, uid1, uid2):
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)
        return Friend.objects.create(uid1=uid1, uid2=uid2)