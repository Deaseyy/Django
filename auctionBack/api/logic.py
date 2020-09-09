# from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
import uuid
from calendar import timegm
from datetime import datetime

from rest_framework_jwt.settings import api_settings


def get_token(user):
    # jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token

# 因为该方法payload载荷生成需要user对象有username属性，重写它
def jwt_payload_handler(user):
    # username_field = get_username_field()
    # username = get_username(user)
    # warnings.warn(
    #     'The following fields will be removed in the future: '
    #     '`email` and `user_id`. ',
    #     DeprecationWarning
    # )
 # todo：payload默认使用username,改成phone
    payload = {
        'user_id': user.pk,
        'phone': user.phone,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }

    if hasattr(user, 'email'):
        payload['email'] = user.email
    if isinstance(user.pk, uuid.UUID):
        payload['user_id'] = str(user.pk)

    # payload['username_field'] = username
    payload['phone'] = user.phone

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    return payload