# server.py TCP sort mixed server

from SocketServer import *
from MysqlPython import *
import re
from hashlib import sha1

class MyTcpServer(ForkingMixIn,TCPServer):
    pass

# re define handler, to handle data from client
class Handler(StreamRequestHandler):
    def handle(self)
        print("Connected from", self.request.etpeername())
        While True:
            self.client_data = self.request.recv(1024)
            data1 = self.client_data.decode()
            if not self.client_datadata:
                break
            print(self.client_data.decode())
            self.request.send(b'recieved')
            # check the data to categorize data
            if re.findall(r"1 \S{1,25}",data1): # name check
                data2 = data1.split(" ")[1]
                if not self.user_name_check(data2):
                    self.request.send(b'name check False')
                elif self.user_name_check(data2):
                    self.request.send(b'name check True')

            elif re.findall(r"2 \S{1,25} \S{1,15}",data1): # password check
                name = data1.split(" ")[1]
                password = data1.split(" ")[2]
                if self.password_check(name,password):
                    self.request.send(b'password check True')
                elif not self.password_check(name,password):
                    self.request.send(b'password check False')

            elif re.findall(r"3 \S+ \S+",data1): # sign in
                name = data1.split(" ")[1]
                password = data1.split(" ")[2]
                self.sign_in(name,password)

            elif re.findall(r"9 \S{1,25}",data1): #vocabulary search
                vocabulary_search(data1)


    def user_name_check(self,data):
        m = MySqlPy("dict_user")
        sql = "select * from userinfo where user_name = %s"
        if m.MySelectAll(sql,[data]):
            return True
        else:
            return False

    def password_check(self,name,password):
        m = MySqlPy("dict_user")
        sql = "select password from userinfo where user_name = %s"
        result = m.MySelectAll(sql,[name])
        s1 = sha1()  
        s1.update(password.encode("utf8"))  
        pwd = s1.hexdigest()  
        if pwd == result:
            return True
        else:
            return False 

    def sign_in(self,name,password):
        s1 = sha1()  
        s1.update(password.encode("utf8"))  
        pwd = s1.hexdigest()
        sql = "insert into userinfo(user_name,password) values (%s,%s);"
        m = MySqlPy("dict_user")
        m.MyExecute(sql,[name,pwd])




    def vocabulary_search(self,data):
        pass
        # return(vocabulary_meaning) 



def main():
    server_addr = ("0.0.0.0", 8888)
    dict_server = MyTcpServer(server_addr,Handler)
    dict_server.serve_forever()

if __name__ == '__main__':
    main()

