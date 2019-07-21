# vocabulary_to_sql.py

from MysqlPython import *
import re


def dict_to_sql():
    m = MySqlPy("dict_user")
    sql = "insert into dictionary values (%s,%s)"
    f = open("dict.txt")
    for line in f:
        L = line.split(" ",1)
        word = L[0]
        try:
            meaning= L[1].lstrip()
        except Exception as e:
            meaning = "null"
        m.MyExecute(sql,[word,meaning])
        print(word)

dict_to_sql()