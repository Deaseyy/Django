
from rest_framework.exceptions import APIException


class ParamsException(APIException):

    # def __new__(cls, *args, **kwargs):
    #     return 对象

    def __init__(self, msg):
        self.detail = msg

