import json
import os.path
import socket
import struct
import subprocess

share_dir = r"C:\Users\czj\Desktop\python\socket111\文件传输\server\share\/"


def put(cmds, conn):


def get(cmds, conn):
    filename = cmds[1]
    # 以 “读”方式打开文件，读取文件内容 发送给客户端
    # 制作固定长度的报头
    header_dic = {
        "filename": filename,
        "md5": "",
        "file_size": os.path.getsize(r'%s%s' % (share_dir, filename))
    }
    header_json = json.dumps(header_dic)
    header_bytes = header_json.encode("utf-8")
    header_len = struct.pack("i", len(header_bytes))
    # 先发送报头长度
    conn.send(header_len)
    # 再发报头
    conn.send(header_bytes)

    # 发送真实信息给客户端
    with open('%s%s' % (share_dir, filename), "rb") as f:
        # conn.send(f.read())
        for line in f:
            conn.send(line)  # 一行一行发，避免文件太多占满内存


def run():
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
                # 接受命令
                date = conn.recv(8096)  # b'get 1.txt'
                #  解析命令 提取参数
                cmds = date.decode("utf-8").split()  # ["get","1.txt"]
                if cmds[0] == 'get':
                    get(cmds, conn)
                if cmds[0] == 'put':
                    put(cmds, conn)




            except ConnectionResetError:  # 防止死循环   仅限win系统
                break
        # 挂电话
        conn.close()
    # 关机
    phone.close()


if __name__ == '__main__':
    run()
