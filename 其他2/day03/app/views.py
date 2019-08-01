from django.db.models import Avg, Sum, Count, Max, Min, F, Q
from django.shortcuts import render
from django.http import HttpResponse

from app.models import Student, StuInfo, Grade, Course


def hello(request):

    return HttpResponse('hello django')


def add_stu(request):
    # 新增数据
    # flask-sqlalchemy: db.session.add(对象)
    # 第一种: save()
    # stu = Student()
    # stu.s_name = 'xiaoming'
    # stu.save()
    # 第二种: create()
    # flask：Student.query
    # django ORM: Student.objects
    Student.objects.create(s_name='xiaohua', s_age=23)
    return HttpResponse('创建学生信息成功')


def sel_stu(request):
    # 查询数据
    # filter()
    stus = Student.objects.filter(s_name='xiaohua1').all()
    stu = stus.first()
    print(stu)
    stu = Student.objects.filter(s_name='xiaohua1').first()
    print(stu)
    # get(条件)
    # 1. 条件必须成立，否则报DoesNotExist
    # 2. 条件查询的结果必须唯一，否则也会报错
    # stu = Student.objects.get(s_name='xiaohua')
    # stu = Student.objects.get(s_age=16)
    stu = Student.objects.filter(s_age=16).first()
    print(stu)

    # exclude(条件) 过滤不满足条件的数据
    stus = Student.objects.exclude(s_age=18).all()
    print(stus)

    # exists(条件): 判断查询条件是否有值，有值则返回true
    stus = Student.objects.filter(s_age=20).exists()
    stus = Student.objects.filter(s_age=20).all()
    len(stus)
    print(stus)

    # count(): 计算满足条件的结果的条数
    stus = Student.objects.all().count()
    print(stus)

    # values()
    stus = Student.objects.all().values('id', 's_name')
    # a = 0
    # for stu in stus:
    #     if stu.yuwen > 80:
    #         a += 1
    print(stus)

    # order_by(): 排序
    stus = Student.objects.all().order_by('-id')
    print(stus)

    # 模糊查询， contains
    # sqlalchemy： filter(模型.s_name.__contains(值))
    # django orm: filter(s_name__contains=‘值’)
    stus = Student.objects.filter(s_name__contains='xiao').all()
    print(stus)
    stus = Student.objects.filter(s_name__startswith='xiao').all()
    print(stus)
    stus = Student.objects.filter(s_name__endswith='xiao').all()
    print(stus)

    # 大于gt  大于等于gte  小于lt  小于等于lte
    # 不存在: >  <  >=  <=
    stus = Student.objects.filter(s_age__gt=17).all()
    # stus = Student.objects.filter(s_age > 17).all()
    print(stus)

    # sqlalchemy: in_([])
    # django orm: 字段__in
    stus = Student.objects.filter(id__in=[1, 2]).all()
    stus = Student.objects.exclude(id__in=[1, 2]).all()
    stus = Student.objects.exclude(pk__in=[1, 2]).all()
    print(stus)

    # 聚合 aggregate()
    # select avg(s_age) from student;
    stus = Student.objects.all().aggregate(Avg('s_age'))
    print(stus)

    # 过滤语文大于数学的成绩的学生信息
    # sql: select * from student where yuwen > math;
    # stus = Student.objects.filter(yuwen__gt=F('math')).all()
    stus = Student.objects.filter(yuwen__lt=F('math') - 20).all()
    print(stus)

    # 且
    stus = Student.objects.filter(s_name__contains='xiao',
                                  s_age__lt=18).all()
    stus = Student.objects.filter(s_name__contains='xiao').\
        filter(s_age__lt=18).all()
    # 或 Q() |
    stus = Student.objects.filter(Q(s_name__contains='xiao')
                                  |
                                  Q(s_age__lt=19)).all()
    print(stus)
    # 非 [^]  ~
    stu = Student.objects.filter(s_age__gt=16).all()
    stu = Student.objects.exclude(s_age__lte=16).all()
    stu = Student.objects.filter(~Q(s_age__lt=16)).all()
    stu = Student.objects.exlude(~Q(s_age__lt=16)).all()

    return HttpResponse('查询数据成功')


def del_stu(request):
    # 删除数据, delete()
    stu = Student.objects.filter(s_name='xiaohua').first()
    stu.delete()
    # 批量删
    Student.objects.filter(s_name='xiaoming').delete()
    return HttpResponse('删除数据成功')


def update_stu(request):
    # 更新数据
    # save(), auto_now定义的字段会自动更新
    stu = Student.objects.filter(s_name='xiaohua').first()
    stu.s_age = 18
    stu.save()
    # update(), auto_now定义的字段不会自动更新
    Student.objects.filter(s_name='xiaohua').update(s_age=16)
    return HttpResponse('修改数据成功')


def add_info(request):
    # 拓展表stu_info中加入数据
    stuinfo = StuInfo()
    stuinfo.phone = '18661388756'
    stuinfo.address = 'xx省xx市xx区xx街道'
    stuinfo.save()
    # 分配关联关系
    stu = Student.objects.get(s_name='xiaoming')
    # 第一种:   对象.外键关联字段 = 关联对象
    stu.info = stuinfo
    # 第二种:   对象.外键关联字段_id = 主键值
    stu.info_id = stuinfo.id
    stu.save()
    return HttpResponse('创建拓展表信息成功')


def sel_info_by_stu(request):
    # 通过学生找拓展表内容
    stu = Student.objects.filter(s_name='xiaoming').first()
    print(stu.info)
    return HttpResponse('查询成功')


def sel_stu_by_info(request):
    # 通过手机号18661388756找人
    stu_info = StuInfo.objects.filter(phone='18661388756').first()
    # 查询学生信息
    # 第一种: 没有定义related_name参数时，拓展表对象.关联表的模型名称的小写
    stu_info.student
    # 第二种: 定义了related_name参数时，拓展表对象.related_name参数
    stu_info.stu
    return HttpResponse('查询成功')


def add_grade(request):
    # 新增班级数据
    names = ['Python班级', 'Java班级', 'Php班级', 'Ios班级']
    for name in names:
        g = Grade()
        g.g_name = name
        g.save()
    return HttpResponse('新增班级数据成功')


def add_stu_grade(request):
    # 给指定学生分配班级
    stus = Student.objects.filter(s_name__in=['xiaoming',
                                              'xiaohua']
                                  ).all()
    grade = Grade.objects.get(g_name='Python班级')
    for stu in stus:
        stu.g_id = grade.id
        stu.g = grade
        stu.save()
    return HttpResponse('分配学生班级信息成功')


def sel_stu_by_grade(request):
    # 通过班级查询学生信息
    g = Grade.objects.filter(g_name='Python班级').first()
    # 第一种: 没有定义related_name参数时，一的一方对象.多的一方模型名称小写_set
    g.student_set.all()
    # 第二种: 定义了related_name参数时，一的一方对象.related_name参数
    g.stu.all()
    return HttpResponse('通过班级查询学生信息成功')


def on_delete_stu(request):
    # models.CASCADE表示级联关系，删除主键的信息，关联的外键也被删掉
    # models.SET_NULL表示主键删除时外键置空处理
    # models.PROTECT表示主外键有对应的关联关系时，主键不让删

    # stu_info = StuInfo.objects.filter(phone='18661388756').first()
    # stu_info.delete()
    g = Grade.objects.get(g_name='Php班级')
    g.delete()
    # Student.objects.filter(pk=2).delete()
    return HttpResponse('删除成功')


def add_cou(request):
    names = ['大学英语', '大学语文', '高数', '模电', 'VHDL']
    for name in names:
        cou = Course()
        cou.c_name = name
        cou.save()
    return HttpResponse('添加课程成功')


def sel_cou_by_stu(request):
    # 通过学生查询课程
    stu = Student.objects.filter(s_name='xiaoming').first()
    stu.c.all()
    return HttpResponse('查询成功')


def sel_stu_by_cou(request):
    # 通过课程查询学生信息
    cou = Course.objects.get(c_name='大学英语')
    # 第一种: 没有定义related_name参数时
    cou.student_set.all()
    # 第二种: 定义了related_name参数时
    cou.stu.all()
    return HttpResponse('查询成功')


def stu_cou(request):
    # 操作课程和学生之间的中间表
    stu = Student.objects.get(s_name='xiaoming')
    cous = Course.objects.filter(c_name__in=['大学英语', 'VHDL'])
    print(stu.c.all())
    for cou in cous:
        # add：向中间表中添加数据
        # stu.c.add(cou)
        # remove: 删除中间表中的数据
        stu.c.remove(cou)
    print(stu.c.all())
    return HttpResponse('学生选课成功')


def index(request):
    stus = Student.objects.all()
    content_h2 = '<h2>我是<span style="color:red;">h2</span>标签</h2>'
    return render(request, 'index.html', {'stus': stus, 'content_h2': content_h2})
