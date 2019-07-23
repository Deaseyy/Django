'''celery初始化'''

import os
from celery import Celery

from worker import config


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swiper.settings')  # 设置系统环境变量, 这样celery才能去django环境中找任务

celery_app = Celery('swiper')
celery_app.config_from_object(config)
celery_app.autodiscover_tasks()  # 自动去发现django项目中哪些是异步的,哪些是被celery_app装饰过的