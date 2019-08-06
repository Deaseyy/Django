import socket

# 1.创建UDP的socket对象
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. 收发数据
while True:
    # 发送数据
    data = input('>').encode()
    client_socket.sendto(data, ('10.20.153.87', 8888))

    # 接收数据
    recv_data, addr = client_socket.recvfrom(1024)
    print('服务端说：', recv_data.decode())


