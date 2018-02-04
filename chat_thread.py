# -*- coding=utf-8 -*-
# 2018/2/3,14:44
import socket
import time
import threading
import re

"""实现一个基于tcp多任务的全双工聊天器
1、第一次连接输入的为用户名
2、发送信息时 有格式要求 to someone content"""

class TcpSocket(object):
    """创建一个tcp服务器，实现监听功能"""
    def __init__(self):
        """初始化"""
        # 创建一个tcp的socket
        self.tcp_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # 绑定端口
        self.port = 8090
        self.host = ""
        self.ADDR = (self.host,self.port)
        self.tcp_server.bind(self.ADDR)
        # 设置端口的复用性
        self.tcp_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        # 设置监听
        self.tcp_server.listen(128)
        # 设置一个字典 存储tcp客户端返回的套接字，以fineno为key
        self.dic = {}
        # 定义一个列表存储用户名和客户端的fineno
        self.user_list = list()

    def run_forever(self):
        while True:
            client,addr = self.tcp_server.accept()
            # 将返回的客户端的套接字存储在字典中
            try:
                name = client.recv(1024)
                if name:
                    name = name.decode("gbk")
                    add = (name,client.fileno())
                    print("创建用户名成功")
                    self.user_list.append(add)
                    self.dic[client.fileno()] = client
                    self.show_online(client,name)
                    # 创建一个线程
                    print("创建线程成功")
                    try:
                        t1 = threading.Thread(target=self.handle,args=(client,name))
                        t1.start()
                    except:
                        pass

            except Exception as e:
                print(e)
            else:
                pass
                # 创建一个线程 执行socket的操作
                # threading.Thread(target=)

    def show_online(self,client,name):
        """把在线的客户端发送一下"""
        for name,fd in self.user_list:
            msg = "%s : online\n"%name
            client.send(msg.encode("gbk"))

    def handle(self,client,name):
        print("开始循环")
        while True:
            msg = client.recv(1024).decode("gbk")
            if msg == False:
                # 删除字典中的套接字
                del self.dic[client.fileno()]
                # 删除列表中的用户名
                self.user_list.remove((name,client.fileno()))
                # 终止循环
                print("线程结束")
                # break
                client.close()
                return
            # 客户端输入机制 to name content
            res = re.match("[^ ]* ([^ ]*) (.*)",msg)
            if res:
                # if res.group(1):
                to_name = res.group(1)
                for name2,fd in self.user_list:
                    if name2 == to_name:
                        content = res.group(2)
                        self.dic[fd].send(content.encode("gbk"))
                        break
                else:
                    content = "user not on line"
                    client.send(content.encode("gbk"))
                    self.show_online(client,name)
            else:
                content = "格式错误"
                client.send(content.encode("gbk"))

if __name__ == '__main__':
    tcp = TcpSocket()
    tcp.run_forever()