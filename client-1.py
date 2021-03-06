'''
Author: zhonzxad
Date: 2021-11-21 14:30:32
LastEditTime: 2021-11-25 20:57:10
LastEditors: zhonzxad
'''
#-*- coding:utf-8 -*-

import socket
import time
from threading import Thread, local

BUFFSIZE=2048
splitChar = "|"

class ClientObj():
    def __init__(self, ipstr, localhost):
        self.ip = ipstr
        self.localhost = localhost
        self.sock = socket.socket()
        self.sock.connect((self.ip, 1334, ))
        self.first = True
        self.isfinish = False

    def __del__(self):
        pass

    def SendMsg(self, hostip):
        while True:
            message = input("输入要发送的消息: ")
            if message == "exit":
                self.sock.sendall(b"exit")
                self.isfinish = True
                break
            else:
                if len(message) == 0 or \
                    message == " ":
                    continue
                if message.find(splitChar) == -1:
                    print("请输入准确的接受方的IP地址,或者检查输入格式")
                    continue

                self.sock.sendall(str.encode(message))
        
        self.sock.close()

    def RecMsg(self):
        while True:
            if self.isfinish:
                break

            data = self.sock.recv(BUFFSIZE).decode('utf-8')

            try:
                if data.find(splitChar) == -1:
                    RecIp = self.ip
                    message = data
                else:
                    RecIp, message = data.split(splitChar)
            except:
                print("收到错误的消息，丢弃")
                continue
            
            if RecIp != self.localhost:
                continue
            if len(message) == 0 or \
                message == " ":
                continue
            if message == "exit":
                break

            if self.first:
                print(message)
                self.first = False
            else:
                print("\n收到消息, " + message + "\n输入要发送的消息: ", end='')

def get_host_ip():
    """
    查询本机ip地址
    :return:
    """
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip=s.getsockname()[0]
    finally:
        s.close()

    return ip
        

if __name__ == "__main__":
    localhost = get_host_ip()
    ip = input("本机ip地址为:{},请输入服务端的ip地址: \n".format(localhost))  #
    obj = ClientObj(ip, localhost)
    thread_Send = Thread(target=obj.SendMsg, args=(localhost,))
    thread_Rev  = Thread(target=obj.RecMsg)
    thread_Rev.start()
    time.sleep(0.01)
    thread_Send.start()
