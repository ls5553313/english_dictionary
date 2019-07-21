# client.py
# tcp_client.py
from socket import *
import os
import time


class DictClient():
    def __init__(self, addr):
        self.sockfd = socket(AF_INET, SOCK_STREAM)
        self.sockfd.connect(server_addr)


    def login_data_handle(self):  # login data handle, categorize
        while True:
            print('''1.login
2.sign in
3.quit''')

            data_input = input("pls select: ")
            if data_input == "1":
                name = str(input("pls input user name: "))
                if self.name_check(name):
                    password = str(input("pls input user password: "))
                    if self.login(name,password):
                        print("login success")
                        break
                    else:
                        print("wrong password!")
                        continue
                else:
                    print("wrong name!")
                    continue

            elif data_input == "2":
                self.signin()
            elif data_input == "3":
                os._exit()
            else:
                print("pls input again!")
                continue

    def name_check(self, name):
        name_send = '1 ' + name
        self.sockfd.send(name_send.encode())
        data_recv = self.sockfd.recv(1024).decode()
        if data_recv == "name check True":
            return True
        else:
            return False

    def login(self, name, password):
        msg_send = '2 ' + name + ' ' + password
        self.sockfd.send(msg_send.encode())
        data_recv = self.sockfd.recv(1024).decode()
        if data_recv == "password check False":
            return False
        else:
            return True

    def signin(self):
        while True:
            name = str(input("pls input user name: "))
            if not self.name_check(name):
                print("name can be used!")
            else:
                print("name cannot be used")
                continue
            password = str(input("pls input user password: "))
            msg_send = '3 ' + name + ' ' + password
            self.sockfd.send(msg_send.encode())
            data_recv = self.sockfd.recv(1024).decode()
            if data_recv == "signed":
                print("signin success")
                break
    
    def close():
        self.sockfd.close()

server_addr = ('127.0.0.1', 8889)

cl = DictClient(server_addr)
cl.login_data_handle()

# 关闭套接字
