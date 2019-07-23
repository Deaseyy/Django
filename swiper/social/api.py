from django.shortcuts import render

# Create your views here.
from common import errors, keys
from lib.cache import rds
from lib.http import render_json
from social import logic
from social.models import Swipe
from swiper import config
from vip.logic import need_perm


def get_recommend_list(request):
    '''获取推荐列表'''
    user = request.user
    users = logic.get_rcmd_list(user)
    data = [user.to_dict() for user in users]
    return render_json(data=data)


def like(request):
    '''操作为喜欢'''
    user = request.user
    sid = request.POST.get('sid')

    # 喜欢+5分
    key = keys.HOT_RANK_KEY % sid
    # redis的sorted_set类的操作(需要将score放key前面),
    # 第一次执行创建这个有序集合KEY-value, 后面每次执行在原value上加上指定分数
    rds.zincrby(config.RANK_KEY, config.LIKE_SCORE, key)

    # 在swipe中创建一条记录
    flag = logic.like(user.id, int(sid))
    if flag:
        return render_json(data={'matched': True})
    return render_json(data={'matched': False})


def dislike(request):
    user = request.user
    sid = request.POST.get('sid')

    # 不喜欢减5分
    key = keys.HOT_RANK_KEY % sid
    rds.zincrby(config.RANK_KEY, config.DISLIKE_SCORE, key)

    Swipe.dislike(uid=user.id, sid=int(sid))
    return render_json()


@need_perm('superlike')
def superlike(request):
    user = request.user
    # 在swipe中创建一条记录.
    sid = request.POST.get('sid')

    # 超级喜欢加7分
    key = keys.HOT_RANK_KEY % sid
    rds.zincrby(config.RANK_KEY, config.SUPERLIKE_SCORE, key)

    flag = logic.superlike(user.id, int(sid))
    if flag:
        return render_json(data={'matched': True})
    return render_json(data={'matched': False})


# @need_perm('rewind')
def rewind(request):
    '''反悔(每天允许返回 3 次) 只允许返回上一次操作'''
    # 删除最近滑动记录
    # 如果有好友关系的话, 好友关系也要撤销
    # 每次执行返回操作之前, 先从缓存中取出来已经操作次数, 小于3就可以继续操作
    user = request.user
    # flag = logic.rewind(user)
    # if flag:
    #     return render_json()
    # return render_json(code=errors.REWIND_ERR, data='今天反悔次数用尽')
    logic.rewind(user)
    return render_json()


@need_perm('liked_me')
def liked_me(request):
    '''查看喜欢过我的人'''
    user = request.user
    users = user.liked_me()
    data = [u.to_dict() for u in users]
    return render_json(data=data)


def get_top_n(request):
    '''查看人气排行榜'''
    data = logic.get_top_n()
    return render_json(data=data)
