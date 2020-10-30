import flask
from flask import Flask,render_template,request
import os
import urllib3
import requests
import pymysql
app = Flask(__name__)

# 打开数据库连接
db = pymysql.connect("localhost", "ytuwind", "XC4djtPwCDjsfGZG", "ytuwind", charset='utf8' )
def SendSQL(sql):
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()  # 接受返回结果行
    # for row in results:
    cursor.close()
    return results

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
    app.run()