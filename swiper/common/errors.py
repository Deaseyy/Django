'''定制错误码'''

SMS_ERROR = 1000  # 短信发送错误
VCODE_ERROR = 1001 # 短信验证码输入错误
LOGIN_REQUIRED = 1002 # 未登录
USER_NOT_EXIST = 1003 # 用户不存在
PROFILE_ERR = 1004  # 个人资料修改失败
AVATAR_ERR = 1005  # 上传头像失败

REWIND_ERR = 1006 # 本日反悔次数用尽


# Error改写成类形式
# 基类
class LogicErr(Exception):
    code = None
    data = None

    def __str__(self):
        return f'<{self.__class__.__name__}>yds'


def gen_error_class(name, code, data):
    # type() 可以创建新的类 type(新类名, (继承的类,可多个,元组形式), {类属性})
    return type(name, (LogicErr,), {'code':code, 'data':data})


## 生成各种异常类
SmsError = gen_error_class('SmsError', code=1000, data='短信发送错误')
VcodeError = gen_error_class('VcodeError', code=1001, data='验证码错误')
# process_exception只能处理视图函数中抛出的异常, 下面俩为中间中的异常,不能抛出,需正常返回json
# LoginRequired = gen_error_class('LoginRequired', code=1002, data='请登录')
# # UserNotExist = gen_error_class('UserNotExist', code=1003, data='用户不存在')

ProfileErr = gen_error_class('ProfileErr', code=1004, data='个人资料错误')
AvatarErr = gen_error_class('AvatarErr', code=1005, data='头像上传失败')
RewindErr = gen_error_class('RewindErr', code=1006, data='超过最大反悔次数')

PermissionRequired = gen_error_class('PermissionRequired', code=1007, data='权限不足,请充值')


# print(SmsError.data)
# print(SmsError)
