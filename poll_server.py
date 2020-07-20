"""
基于poll方法实现IO并发
"""

from socket import *
from select import *

# 全局变量
HOST = "0.0.0.0"
PORT = 8889
ADDR = (HOST,PORT)

# 创建tcp套接字
tcp_socket = socket()
tcp_socket.bind(ADDR)
tcp_socket.listen(5)

# 设置为非阻塞
tcp_socket.setblocking(False)

p = poll() # 建立poll对象
p.register(tcp_socket,POLLIN) # 初始监听对象

# 准备工作，建立文件描述符 和 IO对象对应的字典  时刻与register的IO一致
map = {tcp_socket.fileno():tcp_socket}

# 循环监听
while True:
    # 对关注的IO进行监控
    events = p.poll()
    # events--> [(fileno,event),()....]
    for fd,event in events:
        # 分情况讨论
        if fd == tcp_socket.fileno():
            # 处理客户端连接
            connfd, addr = map[fd].accept()
            print("Connect from", addr)
            connfd.setblocking(False) # 设置非阻塞
            p.register(connfd,POLLIN) # 添加到监控
            map[connfd.fileno()] = connfd # 同时维护字典
        elif event & POLLIN:
            # 收消息
            data = map[fd].recv(1024)
            if not data:
                # 客户端退出
                p.unregister(fd) # 移除关注
                map[fd].close()
                del map[fd] # 从字典也移除
                continue
            print(data.decode())
            p.register(fd,POLLOUT) # 关注写
        elif event & POLLOUT:
            map[fd].send(b'OK')
            p.register(fd, POLLIN)







