import socket

#  买手机
import struct

phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 拨号
phone.connect(("127.0.0.1", 8088))

# 发收消息
while True:
    # 1. 发消息
    msg = input(">>").strip()  # 去空格
    if not msg: continue
    phone.send(msg.encode("utf-8"))
    # 先接受报头
    header = phone.recv(4)
    # 从报头中解析信息
    total_size = struct.unpack("i", header)[0]

    # 接受真是信息
    recv_size = 0
    recv_date = b''
    while recv_size < total_size:
        res = phone.recv(1024)
        recv_date += res
        recv_size += len(res)
    print(recv_date.decode("GBK"))

# 关闭
phone.close()
