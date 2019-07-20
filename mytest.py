# mytest.py
from MysqlPython import * 
from hashlib import sha1

def user_name_check(data):
    m = MySqlPy("dict_user")          
    sql = "select * from userinfo where user_name = %s"
    if m.MySelectAll(sql,[data]):
        return True
    else:
        return False

def password_check(name,password):
        m = MySqlPy("dict_user")
        sql = "select password from userinfo where user_name = %s"
        result = m.MySelectAll(sql,[name])
        s1 = sha1()  # 创建sha1加密对象
        s1.update(password.encode("utf8"))  # 指定编码
        pwd2 = s1.hexdigest()  # 返回16进制加密结果
        print(result)
        print(pwd2)

def sign_in(name,password):
        s1 = sha1()  
        s1.update(password.encode("utf8"))  
        pwd = s1.hexdigest()
        sql = "insert into userinfo(user_name,password) values (%s,%s);"
        m = MySqlPy("dict_user")
        m.MyExecute(sql,[name,pwd])



sign_in("admin","123")
#password_check("admin","admin")
# a = user_name_check("admin")
# print(a)