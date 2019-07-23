'''celery配置文件'''

broker_url = 'redis://127.0.0.1:6379/0'   # (消息中间件)任务调度队列,接收任务,使用redis
broker_pool_limit = 100  # Borker 连接池, 默认是10

timezone = 'Asia/Shanghai'
accept_content = ['pickle', 'json']

task_serializer = 'pickle'
result_expires = 3600  # 任务过期时间

result_backend = 'redis://127.0.0.1:6379/0'   # 任务结果存储
result_serializer = 'pickle'
result_cache_max = 1000  # 任务结果最大缓存数量

# 日志等级
worker_redirect_stdouts_level = 'INFO'