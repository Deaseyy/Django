import socket

# 1.创建UDP的socket对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. 绑定IP和PORT
server_socket.bind(('10.20.153.87', 8888))

# 3. 收发数据
while True:
    data, addr = server_socket.recvfrom(1024)  # 等待接收数据，会阻塞程序
    print('客户端[%s]说：' % str(addr), data.decode())

    server_socket.sendto('今晚吃鸡'.encode(), addr)  # 发送数据

