import json
import socket
import struct

#  买手机
phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 拨号
phone.connect(("127.0.0.1", 8088))
# 发收消息
while True:
    # 发消息
    msg = input(">>").strip()  # 去空格
    if not msg: continue
    phone.send(msg.encode("utf-8"))
    # 先取报头长度
    obj = phone.recv(4)
    header_len = struct.unpack("i", obj)[0]
    # 再收报头
    header_bytes = phone.recv(header_len)
    # 从报头中解析信息
    header_json = header_bytes.decode("utf-8")
    header_dic = json.loads(header_json)
    total_size = header_dic["total_size"]

    # 接收真实信息
    recv_size = 0
    recv_date = b''
    while recv_size < total_size:
        res = phone.recv(1024)
        recv_date += res
        recv_size += len(res)
    print(recv_date.decode("GBK"))

# 关闭
phone.close()
