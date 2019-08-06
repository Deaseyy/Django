import socket

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 1：版本号
# 1：表示包号，可以自定义
# 宝强: 表示用户名
# ROCK: 表示主机名
# 32: 表示发送消息
# hehe: 发送内容
msg = '1:1:宝强:ROCK:32:hehe'.encode('gbk')
udp.sendto(msg, ('10.20.153.87', 2425))

udp.close()
