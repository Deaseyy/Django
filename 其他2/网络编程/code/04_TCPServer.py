import socket

# 1. 创建socket对象
# 2. 绑定IP和PORT
# 3. 设置监听数（客户端连接数）
# 4. 等待客户端连接
# 5. 连接成功后，则可以发送和接收客户端数据
# 6. 关闭连接

# 1. 创建socket对象
#   AF_INET: ipv4,  AF_INET6:ipv6
#   SOCK_STREAM：TCP,  SOCK_DGRAM: UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. 绑定IP和PORT
server_socket.bind(('10.20.153.87', 6666))

# 3. 设置监听数（客户端连接数）
server_socket.listen(5)

# 4. 等待客户端连接
#   accept(): 让程序阻塞
print('服务器已启动，等待客户端连接...')
client, addr = server_socket.accept()
# print(client)  # 客户端socket对象
# print(addr)  # 客户端的address

# 5. 连接成功后，则可以发送和接收客户端数据
while True:
    try:
        print('%s连接成功！ 等待客户端发送数据过来....' % str(addr))
        data = client.recv(1024)  # 等待接收数据，会阻塞程序
        print('接收数据成功:', data)

        client.send('今晚吃鸡'.encode())  # 发送数据
    except Exception as e:
        print('Error:', e)
        break

# 6. 关闭连接
# server_socket.close()






