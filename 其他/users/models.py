from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """用户模型类"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

    class Meta:
        db_table = 'ly_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


from luffy.utils.models import BaseModel
from courses.models import Course
class UserCourse(BaseModel):
    pay_choices = (
        (0, '支付宝'),
        (1, '微信支付'),
        (2, '免费活动'),
        (3, '活动赠品'),
        (4, '系统赠送'),
    )
    user = models.ForeignKey(User, related_name='user_courses', on_delete=models.DO_NOTHING,verbose_name="用户")
    course = models.ForeignKey(Course, related_name='course_users', on_delete=models.DO_NOTHING, verbose_name="课程")
    buy_number = models.CharField(max_length=128, null=True, verbose_name="账单号")
    buy_type = models.SmallIntegerField(choices=pay_choices, default=0, verbose_name="购买方式")
    pay_time = models.DateTimeField(null=True, verbose_name="购买时间")
    out_time = models.DateTimeField(null=True, verbose_name="过期时间")

    class Meta:
        db_table = 'ly_user_course'
        verbose_name = '课程购买记录'
        verbose_name_plural = verbose_name