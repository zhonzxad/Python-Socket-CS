#-*- coding:utf-8 -*-
import socket
import socketserver
import time
from threading import Thread

BUFFSIZE=2048
global ip
splitChar = "|"
all_clients = []

class MyServer(socketserver.BaseRequestHandler):
    """
    请求处理的类
    必须继承 BaseRequestHandler 方法
    重写父类里handle()方法
    """
    first = True
    def handle(self):
        if (self.request) not in all_clients:
            all_clients.append(self.request)
        # 发送登录提示
        strmsg = ("*"*8 + "欢迎登录" + "*"*8)
        self.request.sendall(strmsg.encode())
        print("有客户端{}连接了".format(self.client_address[0]))
        while True:
            # 发送方地址
            add, poart = self.request.getpeername()
            # 接收消息,并转换为utf8
            recstr = self.request.recv(BUFFSIZE).decode('utf-8')
            
            if len(recstr) == 0 or \
                recstr == " ":
                continue
            if recstr == "exit":
                break
            
            try:
                sendIp, msg = recstr.split(splitChar)
            except:
                print("收到消息的格式不正确, 丢弃")
                return 0

            print("{}发送消息给{}, 消息长度{}".format(add, sendIp, len(msg)))
            sendmsg = sendIp + splitChar + msg
            for client in all_clients:
                if client._closed: 
                    all_clients.remove(client)
                elif client.getpeername()[0] == sendIp:
                    client.sendall(str.encode(sendmsg))
                    break
                else:
                    continue

        self.request.close()
        print("客户端{}已失去连接".format(self.client_address[0]))

    def MsgHandle(request):
        pass


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

# C:/Users/zxuan/anaconda3/envs/user/python.exe g:/Py_Debug/Socket/client.py
if __name__ == "__main__":
    ip = get_host_ip()
    # 实例化
    server = socketserver.ThreadingTCPServer((ip, 1334, ), MyServer)
    print("服务端启动成功, 等待客户端的连接, 服务端IP地址为: {}".format(ip))
    # 调用serve_forever方法
    server.serve_forever()
    

'''
def serve_forever(self, poll_interval=0.5):
    """
    Handle one request at a time until shutdown.
    Polls for shutdown every poll_interval seconds. Ignores
    self.timeout. If you need to do periodic tasks, do them in
    another thread.
    """
'''
