# server.py TCP sort mixed server

from socketserver import *
from MysqlPython import *
import re
from hashlib import sha1


class MyTcpServer(ForkingMixIn, TCPServer):
    pass

# re define handler, to handle data from client


class Handler(StreamRequestHandler):
    def handle(self):
        print("Connected from", self.request.getpeername())
        while True:
            self.client_data = self.request.recv(1024)
            data1 = self.client_data.decode()
            if not self.client_data:
                break
            print(self.client_data.decode())
            # self.request.send('recieved'.encode())
            # check the data to categorize data
            if re.findall(r"1 \S+", data1):  # name check
                data2 = data1.split(" ")[1]
                if not self.user_name_check(data2):
                    self.request.send('name check False'.encode())
                elif self.user_name_check(data2):
                    self.request.send('name check True'.encode())

            elif re.findall(r"2 \S+ \S+", data1):  # password check
                name = data1.split(" ")[1]
                password = data1.split(" ")[2]
                if self.password_check(name, password):
                    self.request.send('password check True'.encode())
                elif not self.password_check(name, password):
                    self.request.send('password check False'.encode())

            elif re.findall(r"3 \S+ \S+", data1):  # sign in
                name = data1.split(" ")[1]
                password = data1.split(" ")[2]
                self.sign_in(name, password)
                self.request.send('signed'.encode())

            elif re.findall(r"9 \S+", data1):  # vocabulary search
                word = data1.split(" ")[1]
                result = self.vocabulary_search(word)
                if result:
                    self.request.send(result.encode())
                else:
                    self.request.send('cant find the word'.encode())

    def user_name_check(self, data):
        m = MySqlPy("dict_user")
        sql = "select * from userinfo where user_name = %s"
        if m.MySelectAll(sql, [data]):
            return True
        else:
            return False

    def password_check(self, name, password):
        m = MySqlPy("dict_user")
        sql = "select password from userinfo where user_name = %s"
        result = m.MySelectAll(sql, [name])
        s1 = sha1()
        s1.update(password.encode("utf8"))
        pwd = s1.hexdigest()
        if pwd == result[0][0]:
            return True
        else:
            return False

    def sign_in(self, name, password):
        s1 = sha1()
        s1.update(password.encode("utf8"))
        pwd = s1.hexdigest()
        sql = "insert into userinfo(user_name,password) values (%s,%s);"
        m = MySqlPy("dict_user")
        m.MyExecute(sql, [name, pwd])

    def vocabulary_search(self, data):
        m = MySqlPy("dict_user")
        sql = "select meaning from dictionary where word = %s"
        result = m.MySelectAll(sql, [data])
        if result:
            return result[0][0].rstrip()
        else:
            return False


def main():
    server_addr = ("0.0.0.0", 8889)
    dict_server = MyTcpServer(server_addr, Handler)
    dict_server.serve_forever()


if __name__ == '__main__':
    main()
