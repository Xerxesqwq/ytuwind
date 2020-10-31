import flask
from flask import Flask,render_template,request
import os
import urllib3
import requests
import pymysql
app = Flask(__name__)

# 打开数据库连接
db = pymysql.connect("localhost", "ytuwind", "XC4djtPwCDjsfGZG", "ytuwind", charset='utf8' )

'''
方法名：SendSQL()
功能：执行SQL语句并返回执行结果
'''
def SendSQL(sql):
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()  # 接受返回结果行
    # for row in results:
    cursor.close()
    return results

'''
方法名：RegisteredUsers()
功能：注册账号
成功返回 注册的账户ID
失败返回-1
ID默认为6位
'''
def RegisteredUsers(username,password,realname,studentnum,college,major,headimageurl,phonenum,classnum):
    sql = "INSERT INTO `ytuwind`.`yw_users`(`username`, `password`, `realname`, `studentsnum`, `college`, `major`, `headimageurl`, `phonenum`, `classnum`) " \
          "VALUES ("+username+", '"+password+"', '"+realname+"', '"+studentnum+"', '"+college+"', '"+major+"', '"+headimageurl+"', '"+phonenum+"', "+classnum+")"
    res = SendSQL(sql)
    if res == 1:
        print("注册成功")
        return id
    if res == -1:
        print("注册失败")
        return -1




@app.route('/')
@app.route('/index')
def hello_world():
    return render_template('index.html',**locals())

@app.route('/user/<int:id>')
def UserId(id):
    sql = "SELECT * FROM `ytuwind`.`yw_users` WHERE `id` = '"+str(id)+"'"
    user_data = SendSQL(sql)
    print(user_data)



    return render_template('user.html',**locals())

if __name__ == '__main__':
    app.run(host="192.168.3.32")