# -*- coding=utf-8 -*-
# 2018/1/24,16:00
import socket
import gevent
from gevent import monkey

monkey.patch_all() # 打补丁


class Tcp_Socket(object):
    """创建一个tcp的服务器"""
    def __init__(self):
        # 创建一个套接字
        self.tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # 设置服务器的端口的复用性
        self.tcp_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
        # 程序绑定的端口为8090
        self.addr = ("",8090)
        self.tcp_socket.bind(self.addr)
        # 主动套接字变为被动套接字
        self.tcp_socket.listen(128)
        # 创建一个字典，收集监听产生的套接字
        self.socket_dict = dict()


    def run_forever(self):
        """一直接收返回的套接字"""
        while True:
            client_socket,client_addr = self.tcp_socket.accept()
            self.socket_dict[client_addr] = [client_socket,0]
            # print(self.socket_dict) # 每次都会添加成功，但是当连接的某个客户端断开之后，不再返回主循环
            self.__show_all(client_socket,client_addr)
            gevent.spawn(self.handle,client_socket,client_addr)
            # self.handle(client_socket,client_addr)


    def __show_all(self,temp,client_addr):
        """打印所有已连接对象"""
        num = 0
        for addr in self.socket_dict:
            if addr != client_addr:
                msg = "%s    %s:在线"%addr
                temp.send(msg.encode("gbk"))
                num = 1
        if num == 0:
            msg = "仅自己在线：%s,%s"%client_addr
            temp.send(msg.encode("gbk"))

    def handle(self,temp_socket,client_addr):
        num = 1
        while True:
            try:
                if num :
                    num = 0
                    recv_data = temp_socket.recv(1024)
                    """如果值为1，则之前没有收到过，第一次收到的消息，默认为确定交流的对象"""
                    # print(recv_data.decode("gbk"))
                    if recv_data:
                        # self.socket_dict[client_addr][1] = 0s
                        port = recv_data.decode("gbk")
                        print("port:",port)
                        for key,value in self.socket_dict.items():
                            print(key)
                            print(key[1])
                            if key[1] == int(port):
                                print("1111111")
                                self.socket_dict[client_addr][1] = value[0] # 将找到的对象的套接字传给套接字列表中
                                # self.socket_dict[key].send(recv_data)
                                print("添加成功")

                        else:
                            # self.socket_dict[client_addr][1] = 0
                            print("用户不在线")
                    else:
                        msg = "%s %s:用户下线" % client_addr
                        del self.socket_dict[client_addr]
                        temp_socket.close()
                        for key,value in self.socket_dict:
                            if key != client_addr and key:
                                self.socket_dict[key].send(msg.encode("gbk"))

                else:
                    # 已建立连接，两个客户正常通信
                    # print("连接发送")
                    msg = temp_socket.recv(1024)
                    if msg:
                        self.socket_dict[client_addr][1].send(msg)
                    else:
                        msg = "%s %s:用户下线" % client_addr
                        print(msg)
                        temp_socket.close()
                        del self.socket_dict[client_addr]
                        print("删除此地址对应的字典")
                        # 程序停止
                        break
            except Exception as e:
                pass
                    # gevent.spawn(self.communication,client_addr,1,0)
                    # gevent.spawn(self.communication,client_addr,0,1)
                    # gevent.spawn(self.socket_dict[client_addr][1].send(),recv_data)
                    # gevent.spawn(self.socket_dict[client_addr][0].send(),recv_data)

    def communication(self,temp,num1,num2):
        """两个客户端实现通信"""
        while True:
            msg = self.socket_dict[temp][num1].recv(1024)
            print(msg.decode("gbk"))
            if msg:
                self.socket_dict[temp][num2].send(msg)
            else:
                msg = "%s %s:用户下线" % temp
                del self.socket_dict[temp]
                self.socket_dict[temp][num1].close()
                for key, value in self.socket_dict:
                    if key != temp:
                        self.socket_dict[key].send(msg.encode("gbk"))




if __name__ == "__main__":
    t = Tcp_Socket()
    t.run_forever()






