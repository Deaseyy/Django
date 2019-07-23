'''
存放三方配置
'''

# 使用云之讯发送短信
YZX_URL = 'https://open.ucpaas.com/ol/sms/sendsms'

YZX_PARAMS = {
 "sid":"a0dde32eea337c1351c7dc9e590dc469",
 "token":"b427c60ab356aeaa80226e941350b99c",
 "appid":"3b5b2de860b445b1b3240f962c57f5d8",
 "templateid":"441757",
 "param": None,
 "mobile": None,
}


# 七牛云
ACCESS_KEY = ''  # 都需登陆七牛云官网，创建七牛云应用，获取
SECRET_KEY = ''
BUCKET_NAME = ''
QINIU_URL= ''


# 额外配置
REWIND_TIMES = 3  # 滑动的默认可反悔次数


# 排行榜配置
LIKE_SCORE = 5   # 喜欢+5分
DISLIKE_SCORE = -5  # 不喜欢-5分
SUPERLIKE_SCORE = 7  # 超级喜欢+7分

# 排行榜的key
RANK_KEY = 'HOT_RANK'
TOP_N = 10