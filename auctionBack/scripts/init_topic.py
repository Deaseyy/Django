"""在环境变量中加入django配置文件，可单独启动该脚本文件"""

import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

# 将配置文件settings的路径写到DJANGO_SETTINGS_MODULE环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE","auctionBack.settings")
django.setup() # 读取配置
