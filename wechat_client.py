"""
Chat room
env: python 3.7
"""

import os
import sys
from socket import *

# 服务器地址
ADDR = ('127.0.0.1', 8888)

# 接收消息长度
RECV_LEN = 2048

#发送消息
def send_msg(s,name):
    while True:
        try:
            text = input("发言:")
        except KeyboardInterrupt:
            text = 'quit'
        #退出聊天室
        if text == 'quit':
            msg = "Q " + name
            s.sendto(msg.encode(),ADDR)
            sys.exit("退出聊天室")

        msg = "C %s %s"%(name,text)
        s.sendto(msg.encode(),ADDR)

#接收消息
def recv_msg(s):
    while True:
        data,addr = s.recvfrom(RECV_LEN)
        print(data.decode())
        #服务器让客户端另一个进程退出
        if data.decode() == 'EXIT':
            sys.exit("接收消息进程关闭")
        print(data.decode() + "\n发言:",end='')

def main():
    s = socket(AF_INET, SOCK_DGRAM)
    while True:
        name = input("请输入姓名:")
        msg = 'L ' + name
        s.sendto(msg.encode(), ADDR)
        # 等待回应
        data, addr = s.recvfrom(RECV_LEN)
        if data.decode() == 'OK':
            print("您已进入聊天室")
            break
        else:
            print(data.decode())

    #创建新的进程
    pid = os.fork()
    if pid < 0:
        sys.exit("Error process")
    elif pid == 0:
        send_msg(s,name)
    else:
        recv_msg(s)


if __name__ == '__main__':
    main()
