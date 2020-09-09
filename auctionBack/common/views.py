
from sts.sts import Sts
from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView



class CredentialView(APIView):
    """获取临时密钥"""
    def get(self,request,*args,**kwargs):
        config = {
        # 临时密钥有效时长，单位是秒
        'duration_seconds': 1800,
        'secret_id': settings.SECRETID,
        'secret_key': settings.SECRETKEY,
        # 换成你的 bucket(存储桶)
        'bucket': 'auction-1302698597',
        # 换成 bucket 所在地区
        'region': 'ap-shenzhen-fsi',
        # 这里改成允许的路径前缀，可以根据自己网站的用户登录态判断允许上传的具体路径
        # 例子： a.jpg 或者 a/* 或者 * (使用通配符*存在重大安全风险, 请谨慎评估使用)
        'allow_prefix': '*',
        # 密钥的权限列表。简单上传和分片需要以下的权限，其他权限列表请看 https://cloud.tencent.com/document/product/436/31923
        'allow_actions': [
            # 简单上传
            'name/cos:PostObject',  # 上传
            'name/cos:DeleteObject',  # 删除
            # 'name/cos:UploadPart',
            # 'name/cos:UploadPartCopy',
            # 'name/cos:CompleteMultipartUpload',
            # 'name/cos:AbortMultipartUpload',
            # '*'
        ],
        }
        sts = Sts(config)
        response = sts.get_credential()
        return Response(response)
