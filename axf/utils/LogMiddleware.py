import logging
from datetime import datetime

from django.utils.deprecation import MiddlewareMixin


logger = logging.getLogger()

class LogMiddle(MiddlewareMixin):
    def process_request(self,request):
        # 请求进来时的时间
        request.init_time = datetime.now()

    def process_response(self,request,response):
        try:
            # 耗时多长
            count_time = datetime.now()-request.init_time
            # 请求方式
            method = request.method
            # 请求地址
            path = request.path
            # 响应状态吗
            status_code = response.status_code
            # 响应内容
            content = response.content

            logger.info('%s %s %s %s %s' % (count_time, method, path,
                                            status_code,content))
        except Exception as e:
            logger.critical('系统错误:%s' % e)

        return response
