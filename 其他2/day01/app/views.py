from django.shortcuts import render
from django.http import HttpResponse

from app.models import Student


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
    stus = Student.objects.filter(s_name='xiaohua').all()
    stu = stus.first()
    print(stu)
    stu = Student.objects.filter(s_name='xiaohua').first()
    print(stu)
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
