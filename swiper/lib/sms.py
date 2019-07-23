import random

import requests
from django.core.cache import cache

from common import keys
from swiper import config
from worker import celery_app  # 异步任务

# 随机生成验证码
def gen_vcode(size=4):  # size :多长
    '''1000-9999'''
    start = 10 ** (size - 1)
    stop = 10 ** size - 1
    vcode = random.randint(start, stop)
    return vcode


# 发送验证码,去请求官方接口
@celery_app.task
def send_vcode(phone):
    params = config.YZX_PARAMS.copy()  # copy 不改变原配置参数
    params['mobile'] = phone
    vcode = gen_vcode()
    params['param'] = vcode

    # 生成的验证码存入缓存 过期时间600s  (可以保存每个异步任务请求生成的验证码)
    cache.set(keys.VCODE_KEY % phone, str(vcode), timeout=600)
    resp = requests.post(config.YZX_URL, json=params)
    if resp.status_code == 200:  # http请求是否成功
        # ok
        result = resp.json()   # 接收云之讯返回的json数据转字典
        if result['code'] == '000000':
            return 'OK'
        else:
            return result['msg']
    else:
        return '发送短信有误'