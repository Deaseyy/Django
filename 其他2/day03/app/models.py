from django.db import models


class Article(models.Model):
    # 唯一、不能为空且长度不能超过10字符的title字段
    title = models.CharField(max_length=10, unique=True, null=False)
    desc = models.TextField(null=False)
    is_delete = models.BooleanField(default=0)

    class Meta:
        db_table = 'article'


class StuInfo(models.Model):
    phone = models.CharField(max_length=11, null=True)
    address = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'stu_info'


class Grade(models.Model):
    g_name = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = 'grade'


class Course(models.Model):
    c_name = models.CharField(max_length=10, unique=True, verbose_name='课程名')

    class Meta:
        db_table = 'course'


class Student(models.Model):
    # 最大长度为10字符，不能为空，唯一
    s_name = models.CharField(max_length=10, unique=True,
                              null=False, verbose_name='id')
    s_age = models.IntegerField(default=20, verbose_name='年龄')
    # auto_now_add: 创建数据时，默认赋予创建时间
    create_time = models.DateTimeField(auto_now_add=True,
                                       verbose_name='创建时间')
    # auto_now: 修改数据时，默认赋予修改的时间
    operate_time = models.DateTimeField(auto_now=True,
                                        verbose_name='修改时间')
    yuwen = models.DecimalField(max_digits=3, decimal_places=1,
                                null=True, verbose_name='语文成绩')
    math = models.DecimalField(max_digits=3, decimal_places=1,
                               null=True, verbose_name='数学成绩')
    # OneToOneField: 一对一
    info = models.OneToOneField(StuInfo, on_delete=models.CASCADE,
                                null=True, related_name='stu')
    # ForeignKey: 一对多
    g = models.ForeignKey(Grade, on_delete=models.PROTECT,
                          null=True, related_name='stu')
    # ManyToManyField: 多对多
    c = models.ManyToManyField(Course, related_name='stu')

    # TimeField
    # DateField
    # ImageField
    # DecimalField
    # FloatField
    # BooleanField
    # AutoField

    class Meta:
        db_table = 'stu'

