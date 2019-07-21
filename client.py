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
                    if self.login(name, password):
                        print("login success")
                        self.second_interface()
                        break
                    else:
                        print("wrong password!")
                        continue
                else:
                    print("wrong name!")
                    continue

            elif data_input == "2":
                self.signin()
                self.second_interface()
            elif data_input == "3":
                os._exit(1)
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

    def close(self):
        self.sockfd.close()

    def second_interface(self):
        while True:
            print('''1.word search
2.history check
3.quit''')
            try:
                data_input = input("pls select: ")
                if data_input == "1":
                    word = input("pls input a word: ")
                    meaning = self.word_search(word)
                    if meaning != "cant find the word":
                        file = open("client_history.txt", 'a')
                        data_write = word + ",,," + meaning + "\n"
                        file.write(data_write)
                        print(word, "\n", meaning)
                        file.close()
                        continue
                    else:
                        print("cant find the word")
                        continue

                elif data_input == "2":
                    self.show_history()
                elif data_input == "3":
                    try:
                        os.remove("./client_history.txt")
                    except:
                        pass
                    self.login_data_handle()
                else:
                    print("pls input again!")
                    continue
            except:
                print("cant find history!")

    def word_search(self, word):
        word_send = "9 " + word
        self.sockfd.send(word_send.encode())
        meaning = self.sockfd.recv(4096).decode()
        return meaning

    def show_history(self):
        file = open("client_history.txt", 'r')
        i = 0
        for line in file:
            print(line)
        file.close()


server_addr = ('127.0.0.1', 8889)

cl = DictClient(server_addr)
cl.login_data_handle()
