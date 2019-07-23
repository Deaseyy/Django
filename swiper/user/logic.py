import os

from django.conf import settings

from common import keys
from lib.qiniuyun import upload_qiniu
from worker import celery_app


@celery_app.task
def handle_uploaded_file(uid, avatar):
    # 保存到本地
    filename = keys.AVATAR_KEY % uid
    filepath = os.path.join(settings.BASE_DIR, settings.MEDIAS_ROOT, filename)
    with open(filepath, 'wb+') as fp:
        for chunk in avatar.chunks():  # 以防文件太大,可以分段写入
            fp.write(chunk)

    # 上传到七牛云
    upload_qiniu(uid)
