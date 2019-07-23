import os

from django.conf import settings
from qiniu import Auth, put_file  # 需安装七牛云接口库

from common import keys
from swiper import config




#需要填写你的 Access Key 和 Secret Key
access_key = config.ACCESS_KEY
secret_key = config.SECRET_KEY
#要上传的空间
bucket_name = config.BUCKET_NAME


def upload_qiniu(uid):
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 上传后保存的文件名
    filename = keys.AVATAR_KEY % uid
    # 生成上传 Token, 可以指定过期时间
    token = q.upload_token(bucket_name,filename,3600)

    # 要上传文件的本地路径
    filepath = os.path.join(settings.BASE_DIR, settings.MEDIAS_ROOT, filename)
    ret, info = put_file(token, filename, filepath)

    if info.status_code == 200:
        return True
    return False