from django.contrib import admin

from user.models import AXFUser

# 将模型AXFUser交给后台进行管理
admin.site.register(AXFUser)
