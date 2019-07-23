'''
封装返回json的操作
'''
import json

from django.http import HttpResponse
from django.conf import settings

def render_json(code=0, data=None):
    dic = {
        'code': code,
        'data':data
    }

    if settings.DEBUG:
        dic = json.dumps(dic, indent=4, ensure_ascii=False, sort_keys=True) # 开发模式 格式化便于查看
    else:
        dic = json.dumps(dic, separators=[',', ':'], ensure_ascii=False)  # 线上发布, 紧凑便于传输

    return HttpResponse(dic)