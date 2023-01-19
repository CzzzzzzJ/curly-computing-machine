import json
import socket
import struct
import subprocess

#  买手机
phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
phone.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 绑定端口前查看占用
# 绑定手机卡
phone.bind(("127.0.0.1", 8088))  # 端口 0-65535
# 开机
phone.listen(5)  # ”5“ 代表最大挂起的连接数
#  等电话链接
print("waitting.......")
while True:  # 链接循环
    conn, clinet_addr = phone.accept()
    print(clinet_addr)

    # 收发消息
    while True:  # 通信循环
        try:
            date = conn.recv(8096)  # 1024代表接受数据的最大数1024 单位：bytes
            if not date: break  # 防止死循环   仅限Linux系统
            obj = subprocess.Popen(date.decode('utf-8'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout = obj.stdout.read()
            stderr = obj.stderr.read()
            # 制作固定长度的报头
            header_dic = {
                "filename": "a.txt",
                "md5": "",
                "total_size": len(stdout) + len(stderr)
            }
            header_json = json.dumps(header_dic)
            header_bytes = header_json.encode("utf-8")
            header_len = struct.pack("i", len(header_bytes))
            # 先发送报头长度
            conn.send(header_len)
            # 再发报头
            conn.send(header_bytes)

            # 发送真是信息给客户端

            conn.send(stdout + stderr)
        except ConnectionResetError:  # 防止死循环   仅限win系统
            break
    # 挂电话
    conn.close()
# 关机
phone.close()
