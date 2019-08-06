import socket
import threading  # 线程

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('10.20.153.87', 6666))
server_socket.listen(50)


# 5. 连接成功后，则可以发送和接收客户端数据
def socket_thread(client, addr):
    while True:
        try:
            print('%s连接成功！ 等待客户端发送数据过来....' % str(addr))
            data = client.recv(1024).decode()  # 等待接收数据，会阻塞程序
            print('接收%s数据成功:' % str(addr), data)

            client.send('今晚吃鸡'.encode())  # 发送数据
        except Exception as e:
            print('Error:', e)
            break


if __name__ == '__main__':
    while True:
        print('服务器已启动，等待客户端连接...')
        client, addr = server_socket.accept()

        # 开辟一个子线程，子线程的执行函数socket_thread
        t = threading.Thread(target=socket_thread, args=(client, addr))
        t.start()  # 启动线程




