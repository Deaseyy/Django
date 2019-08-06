import socket

# 1. 创建socket对象
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. 主动连接服务端
client_socket.connect(('10.20.153.87', 6666))

# 3. 发送和接收服务端数据
while True:

    # 发送数据给服务端
    data = input('>').encode()
    client_socket.send(data)

    # 接收服务端发过来的数据
    recv_data = client_socket.recv(1024).decode()
    print("接收到服务端的数据：", recv_data)



