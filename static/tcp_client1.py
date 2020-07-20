"""
tcp循环模型客户端1
重点代码
"""

from socket import *

# 创建tcp套接字
tcp_socket = socket()

# 发起连接 连接服务端
tcp_socket.connect(("127.0.0.1",8889))

# 发送消息
while True:
    msg = input(">>")
    if not msg:
        break
    tcp_socket.send(msg.encode()) # 发送字节串
    data = tcp_socket.recv(1024)
    print(data.decode())

tcp_socket.close()