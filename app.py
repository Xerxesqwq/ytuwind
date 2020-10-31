import flask
from flask import Flask,render_template,request,make_response,redirect,url_for
import os
import urllib3
import requests
import pymysql
app = Flask(__name__)

# 打开数据库连接
db = pymysql.connect("localhost", "ytuwind", "XC4djtPwCDjsfGZG", "ytuwind", charset='utf8' )
def SetCookie(cookiename,cookietext,alivetime):
    if alivetime == None :
        alivetime = 3600
    resp = make_response("set cookie success")  # 设置响应体
    resp.set_cookie(cookiename, cookietext, max_age=alivetime)
    return resp
def GetCookie(cookiename):
    cookie_1 = request.cookies.get(cookiename)  # 获取名字为cookiename对应cookie的值
    return cookie_1
def DeleteCookie(cookiename):
    resp = make_response("delete cookie success")
    resp.delete_cookie(cookiename)
    return resp

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

'''
判断是否为登录状态
'''
def IfLogin():
    #print(request.cookies.get('user_name'))
    if request.cookies.get('userid') == None:
        print("未登陆，请先登录")
        return False
    else:
        return True

@app.route('/')
@app.route('/index')
def index():
    if IfLogin() == False:
        return redirect(url_for('user_login'))

    return render_template('index.html',**locals())
@app.route('/register',methods=['POST','GET'])
def user_register():
    return render_template('register.html', **locals())
@app.route('/login',methods=['POST','GET'])
def user_login():
    userid = request.cookies.get("userid")
    if userid==None:#未登录
        return render_template('login.html',**locals())

@app.route('/user/<int:id>')
def UserId(id):
    sql = "SELECT * FROM `ytuwind`.`yw_users` WHERE `id` = '"+str(id)+"'"
    user_data = SendSQL(sql)[0]
    print(user_data)



    return render_template('user.html',**locals())

if __name__ == '__main__':
    app.run(host="192.168.3.32")