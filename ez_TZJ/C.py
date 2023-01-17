import socket

#  买手机
phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 拨号
phone.connect(("127.0.0.1", 8088))

# 发收消息
while True:
    # 1. 发消息
    msg = input(">>").strip()  # 去空格
    if not msg: continue
    phone.send(msg.encode("utf-8"))
    date = phone.recv(1024)
    print(date.decode("GBK"))

# 关闭
phone.close()
