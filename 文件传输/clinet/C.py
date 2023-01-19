import json
import os
import socket
import struct

download_dir = r"C:\Users\czj\Desktop\python\socket111\文件传输\clinet\download\/"


def put(phone, cmds):
    filename = cmds[1]
    # 制作固定长度的报头
    header_dic = {
        "filename": filename,
        "md5": "",
        "file_size": os.path.getsize(r'%s%s' % (download_dir, filename))
    }
    header_json = json.dumps(header_dic)
    header_bytes = header_json.encode("utf-8")
    header_len = struct.pack("i", len(header_bytes))
    # 先发送报头长度
    phone.send(header_len)
    # 再发报头
    phone.send(header_bytes)
    # 发送真实信息给客户端
    with open('%s%s' % (download_dir, filename), "rb") as f:
        for line in f:
            phone.send(line)  # 一行一行发，避免文件太多占满内存


def get(phone):
    # 接受文件内容，以”写“的方式打开新文件并写入
    # 先取报头长度
    obj = phone.recv(4)
    header_len = struct.unpack("i", obj)[0]
    # 再收报头
    header_bytes = phone.recv(header_len)
    # 从报头中解析信息
    header_json = header_bytes.decode("utf-8")
    header_dic = json.loads(header_json)
    total_size = header_dic["file_size"]
    filename = header_dic["filename"]

    # 接收真实信息
    with open('%s%s' % (download_dir, filename), "wb") as f:
        recv_size = 0
        while recv_size < total_size:
            line = phone.recv(1024)
            f.write(line)
            recv_size += len(line)
            print('总大小：%s  已下载：%s' % (total_size, recv_size))


def run():
    #  买手机
    phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 拨号
    phone.connect(("127.0.0.1", 8088))
    # 发收消息
    while True:
        # 发送命令
        cmd = input(">>").strip()  # 去空格
        if not cmd: continue
        phone.send(cmd.encode("utf-8"))
        cmds = cmd.split()
        if cmds[0] == "get":
            get(phone)
        elif cmds[0] == 'put':
            put(phone,cmds)

    # 关闭
    phone.close()


if __name__ == '__main__':
    run()
