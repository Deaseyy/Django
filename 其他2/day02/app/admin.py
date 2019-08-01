from django.contrib import admin

# Register your models here.
from app.models import Article

# 将模型Article交给后台进行管理
admin.site.register(Article)
# admin.site.register(Student)
