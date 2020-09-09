"""一个connection就是一个tcp连接。为了提升tcp连接复用性，在每个连接基础上可以建立多个channel信道，
每个信道都会被指派一个唯一的 ID。同时 RabbitMQ 可以确保每个线程的私密性，就像拥有独立的连接一样。
但考虑到如果数据量过大，会导致连接阻塞，最终这里选择一个connect连接只对应了一个channel信道。
"""
import time

import pika
from django.core.management import BaseCommand
from retrying import retry

class RabbitmqServer(object):
    """封装rabbitmq模块基础类，为业务模块调用"""
    def __init__(self, username, password,serverip, port, virtual_host):
        self.username = username
        self.password = password
        self.serverip = serverip
        self.port = port
        self.virtual_host = virtual_host


    @retry(stop_max_delay=30000, wait_fixed=5000)
    def connect(self):
        # logger.info('into mq connect')
        user_pwd = pika.PlainCredentials(self.username, self.password)
        # logger.info("create mq ...")
        # logger.info("%s,%s,%s,%s,%s" % (self.virtual_host, self.serverip, self.port, self.password, self.username))
        # 创建mq连接
        s_conn = pika.BlockingConnection(
            pika.ConnectionParameters(virtual_host=self.virtual_host, host=self.serverip, port=self.port,
                                      credentials=user_pwd)
        )
        # logger.info('create channel...')
        self.channel = s_conn.channel()
        # logger.info('connect successful')

    def productMessage(self, queue_name, message):
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name, # 将消息发送到指定队列queue_name
            body=message,
            properties=pika.BasicProperties(delivery_mode=2) # 设置消息持久化:将要发送的消息的属性标记为2，表示该消息要持久化
        )

    def expense(self, queue_name, func):
        """
        :param queue_name: 队列名称
        :param func: 回调方法
        """
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(func, queue=queue_name)
        self.channel.start_consuming()  # 启动监听，进入阻塞状态


# 创建一个连接实例
RabbitmqClient = RabbitmqServer("user", "pwd",'ip','mq服务端口',"v_host")


# 自定义的消费者回调 测试rabbitmq服务
def callback(ch, method, properties, body):
    print(" [消费者] Received %r" % body)
    time.sleep(1)
    print(" [消费者] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)#  接收到消息后会给rabbitmq发送一个确认


# 测试
if __name__ == '__main__':
    import json
    RabbitmqClient = RabbitmqServer("user", "pwd",'ip','mq服务端口',"v_host")
    RabbitmqClient.connect()
    data = {"code":3}
    RabbitmqClient.productMessage("test3",json.dumps(data))
    RabbitmqClient.expense("test3",callback)



"""业务使用"""
# 其他业务模块使用时，将RabbitmqClient 这个实例引用过去，如：
def send_to_parse(file_name, file_id, file_url, rule_list, userid):
    data = json.dumps(
        {"file_name": file_name, "file_id": file_id, "file_url": file_url, "rule_list": rule_list, "userid": userid,
         "request_type": "sample"})
    # logger.info("开始发送消息:data:{}".format(str(data)))
    RabbitmqClient.connect()
    RabbitmqClient.productMessage("myqueue", data)
    # logger.info("文件发送完成")

# 执行到这个方法时，就会将消息发送到“myqueue”队列中去



""" django中使用Rabbitmq监听端进行阻塞监听"""
# 使用django命令启动Rabbitmq监听程序，comsumer.py
class Command(BaseCommand):
    def handle(self, *args, **options):
        # 监听消息，将消息处理结果存入数据库并更改数据库中文件状态
        def parse_result_func(ch, method, properties, body):
            # 逻辑程序
            ch.basic_ack(delivery_tag=method.delivery_tag)  # 接收到消息后会给rabbitmq发送一个确认

        # logger.infolog("parse_result_func", "开始监听消息")
        RabbitmqClient.connect()
        RabbitmqClient.expense("myqueue", parse_result_func)


"""
在创建的app下创建文件夹management，在management文件夹下创建文件夹commands，将要执行的文件放到文件夹下，
记得把__init__.py文件一并创建了，init.py是声明这个文件夹是一个包。然后在主目录（就是manage.py文件所在目录）
执行 python manage.py 文件名即可
"""
# 在项目主目录下执行 python manage.py comsumer 就会看到,说明执行成功
# >>> 开始监听消息