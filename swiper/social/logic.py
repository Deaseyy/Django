import datetime
import logging

from django.core.cache import cache

from common import keys, errors
from lib.cache import rds
from social.models import Swipe, Friend
from swiper import config
from user.models import User

logger = logging.getLogger('err')

def get_rcmd_list(user):
    ''' :return [user1,user2,user3] '''
    # 已经滑过的人不能再滑
    swiped_list = Swipe.objects.filter(uid=user.id).only('sid')
    sid_list = [s.sid for s in swiped_list]
    # 推荐用户中不能出现自己
    sid_list.append(user.id)
    # 符合用户个人设置的条件
    current_year = datetime.datetime.now().year
    min_birth_year = current_year - user.profile.max_dating_age
    max_birth_year = current_year - user.profile.min_dating_age
    users = User.objects.filter(location=user.profile.location,
                                birth_year__range=(min_birth_year, max_birth_year),
                                sex=user.profile.dating_sex).exclude(id__in=sid_list)[:20]
    return users


def like(uid, sid):
    '''喜欢'''
    Swipe.like(uid, sid) # 插入数据
    # 对方也喜欢我,添加好友
    if Swipe.has_like_me(sid, uid):
        uid1, uid2 = (uid, sid) if uid < sid else (sid, uid)  # 小的id总是在前, 保证只存入一个对应关系,如: 1和2,2和1
        Friend.make_friends(uid1=uid1, uid2=uid2)
        return True
    return False


def superlike(uid, sid):
    '''超级喜欢'''
    Swipe.superlike(uid, sid)
    # 对方也喜欢我,添加好友
    if Swipe.has_like_me(sid, uid):
        uid1, uid2 = (uid, sid) if uid < sid else (sid, uid)
        Friend.make_friends(uid1=uid1, uid2=uid2)
        return True
    return False


def rewind(user):
    '''反悔'''
    now = datetime.datetime.now()
    key = keys.REWIND_KEY % now.date()
    rewind_times = cache.get(key, 0)  # 取不到值默认给0,使用了0次机会
    if rewind_times < config.REWIND_TIMES:
        # 删除最近执行的滑动记录
        record = Swipe.objects.filter(uid=user.id).latest(field_name='time')  # latest() 根据字段查找最新的记录,  earliest() 最早的记录
        # 判断是否有好友关系
        uid1, uid2 = (user.id, record.sid) if user.id < record.sid else(record.sid,user.id)
        friends = Friend.objects.filter(uid1=uid1, uid2=uid2)
        friends.delete()

        # 更新缓存中本日可反悔次数
        rewind_times += 1
        # 0点重置次数, 设置存在时间为今日剩余时间
        timeout = 86400 - (now.hour) * 60 *60 + now.minute * 60 + now.second
        cache.set(key, rewind_times, timeout)

        # 处理反悔之后的排名得分问题
        key = keys.HOT_RANK_KEY % record.sid
        # if record.mark == 'like':
        #     # 减5分
        #     rds.zincrby(config.RANK_KEY, -config.LIKE_SCORE, key)
        # elif record.mark == 'dislike':
        #     rds.zincrby(config.RANK_KEY, -config.DISLIKE_SCORE, key)
        # else:
        #     rds.zincrby(config.RANK_KEY, -config.SUPERLIKE_SCORE, key)
        # 写法优化，使用模型映射
        mapping = {
            'like': config.LIKE_SCORE,
            'dislike': config.DISLIKE_SCORE,
            'superlike': config.SUPERLIKE_SCORE,
        }
        rds.zincrby(config.RANK_KEY, -mapping[record.mark], key)  # 模型映射

        record.delete()
    else:
        logger.error('exceed the maxmium rewind times')  #日志
        raise errors.RewindErr  # 抛出自定义错误


def get_top_n():
    '''从redis取排名后的id'''
    """
       {
           code:0,
           data: [
               {rank:1,
                score: 100,
                nickname: nickname,
                ...},
               {}
           ]
       }
    """
    # [[b'11', 7.0], [b'2', 5.0], [b'3', -5.0]]
    rank_list = rds.zrevrange('HOT_RANK', 0, -1, withscores=True)
    # 清洗一下数据, 转成int型
    clean_data = [(int(id), int(score)) for (id,score) in rank_list]
    # 从clean中取出id
    id_list = [item[0] for item in clean_data]

    # users = []
    # for id in id_list:
    #     user = User.objects.get(id=id)
    #     user.append(user)

    # 以上写法每个循环都要访问数据库, 推荐以下写法
    # django查询后默认会根据对象id进行排序,是从小到大的.
    users = User.objects.filter(id__in=id_list)
    # 对users排序
    users = sorted(users, key=lambda user:id_list.index(user.id))  # id_list 是已排序的, 根据其中id的下标进行排序

    top_n = []
    for rank, (_, score), user in zip(range(1, config.TOP_N+1), clean_data, users):
        data = dict()
        data['rank'] = rank
        data['score'] = score
        data.update(user.to_dict())
        top_n.append(data)
    return top_n

