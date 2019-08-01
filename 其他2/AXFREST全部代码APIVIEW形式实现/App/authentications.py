from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication

from App.models import AXFUser


class UserTokenAuthentications(BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.query_params.get("token")

            user_id = cache.get(token)

            user = AXFUser.objects.get(pk=user_id)

            return user, token
        except Exception as e:
            print("用户认证失败")
