from lib.orm import model_patch

# 用于给models.Model类动态添加方法， 项目启动就会执行
model_patch()