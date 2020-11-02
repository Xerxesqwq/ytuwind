from flask import Flask,render_template,request,make_response,redirect,url_for,Response
import pymysql
import os
import platform
import datetime
import json
import fun
app = Flask(__name__)
# db = pymysql.connect("localhost", "ytuwind", "XC4djtPwCDjsfGZG", "ytuwind", charset='utf8' )
f = open('config.ini', 'r')
config_text = f.read()
f.close()

config_json = json.loads(config_text)
fun.log(config_json)

# 打开数据库连接
db = pymysql.connect(config_json['db_host'], config_json['db_user'], config_json['db_pass'], config_json['db_name'], charset='utf8')
#读取外部配置
app.debug = config_json['app_debug']




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
    arry = []
    arry.append(-1)
    arry.append(-1)
    arry.append('')
    iskong = SendSQL("SELECT * FROM `ytuwind`.`yw_users` WHERE `username` = '"+username+"' ")
    fun.log(iskong)
    if str(iskong) != "()":
        arry[0] = 2
        arry[2]="用户名重复"
        fun.log("用户名重复")
        return arry
    sql = \
        "INSERT INTO `ytuwind`.`yw_users`(`username`, `password`, `realname`, `studentsnum`, `college`, `major`, `headimageurl`, `phonenum`, `classnum`, `QQnum`) " \
        "VALUES ('"+username+"', '"+password+"', '"+realname+"', '"+studentnum+"', '"+college+"', '"+major+"', '"+headimageurl+"', '"+phonenum+"', '"+str(classnum)+"', '')"
    res = SendSQL(sql)
    if res == 1:
        fun.log("注册成功")
    if res == -1:
        arry[2]=("注册失败")
        fun.log("注册失败")
        return arry

    id = SendSQL("SELECT * FROM `ytuwind`.`yw_users` WHERE `username` = '" + username + "' ")[0][0]
    fun.log(id)
    arry[0]=(res)
    arry[1]=(id)
    arry[2]=("注册成功")
    return arry
'''
判断是否为登录状态
'''
def IfLogin():
    #fun.log(request.cookies.get('user_name'))
    if request.cookies.get('userid') == None:
        fun.log("未登陆，请先登录")
        return False
    else:
        return True

def SearchFromDate(biao,item,key):
    sql="SELECT * FROM `ytuwind`.`"+biao+"` WHERE `"+item+"` LIKE '%"+key+"%'"
    res = SendSQL(sql)
    return res


def RFG(name):#request.form.get
    return request.form.get(name)


@app.route('/')
@app.route('/index')
def index():
    if IfLogin() == False:
        return redirect(url_for('user_login'))
    else:
        userid = request.cookies.get('userid')
    title = "首页"
    userid = request.cookies.get('userid')
    return render_template('index.html',**locals())
@app.route('/register',methods=['POST','GET'])
def user_register():
    if request.method == 'POST':
        username = RFG('username')
        password = RFG('password')
        #messagetext
        realname = RFG('realname')
        studentnum = RFG('studentnum')
        college = RFG('college')
        major = RFG('major')
        headimageurl = "/img/default.jpg"
        phonenum = RFG('phonenum')
        classnum = (RFG('classnum'))
        # fun.log(request.form.items())
        #fun.log(username,password,realname,studentnum,college,major,headimageurl,phonenum,classnum)
        res = RegisteredUsers(username,password,realname,studentnum,college,major,headimageurl,phonenum,classnum)
        userid = res[1]
        messagetext = res[2]
        if res[0]==-2:
            messagetext = "注册失败，请及时联系管理员检查问题。"
    return render_template('register.html', **locals())
@app.route('/login',methods=['POST','GET'])
def user_login():
    if request.method=='POST':
        username = RFG('username')
        password = RFG('password')
        sql = "SELECT * FROM `ytuwind`.`yw_users` WHERE `username` = '"+username+"' AND `password` = '"+password+"'"
        res = SendSQL(sql)
        fun.log(res)
        if str(res)=="()":
            #登录失败
            messagetext="账号或密码错误"
            fun.log("登录失败")
            return render_template('login.html',**locals())
        else:
            userid= res[0][0]
            fun.log(userid)
            response = redirect(url_for('index'))

            response.set_cookie('username', username, max_age=2592000)
            response.set_cookie('userid', str(userid), max_age=2592000)
            return response
    else :
        userid = request.cookies.get("userid")
        if userid==None:#未登录
            return render_template('login.html',**locals())
        else:#已登录
            title = "首页"
            return render_template('index.html',**locals())

def GetUserDateByUserId(userid):
    sql = "SELECT * FROM `ytuwind`.`yw_users` WHERE `id` = '" + str(userid) + "'"
    user_data = SendSQL(sql)[0]
    return user_data
@app.route('/user',methods=['GET'])
def UserId():
    if request.method=='GET':
        userid=RFG('userid')
    if userid==None:
        userid = request.cookies.get('userid')
    fun.log(userid)
    title = "我的"
    user_data = GetUserDateByUserId(userid)
    fun.log(user_data)
    userid=user_data[0]
    username = user_data[1]


    return render_template('user.html',**locals())

@app.route('/function/<function>')
def softfunction(function):
    if IfLogin() == False:
        return redirect(url_for('user_login'))
    else:
        userid = request.cookies.get('userid')
    if function == 'exitlogin':

        response = redirect(url_for('user_login'))
        response.delete_cookie('userid')
        response.delete_cookie('username')
        return response
@app.route('/lostandfoundtasts')
def lostandfound():
    if IfLogin() == False:
        return redirect(url_for('user_login'))
    else:
        userid = request.cookies.get('userid')
    title = "失物招领中心"
    lostandfoundtasts = SendSQL("SELECT * FROM `ytuwind`.`lostandfound`")
    fun.log(lostandfoundtasts)
    return render_template('lostandfoundtasts.html',**locals())
@app.route('/lostandfoundtasts/<id>')
def lostandfoundtasts_id(id):
    if IfLogin() == False:
        return redirect(url_for('user_login'))
    else:
        userid=request.cookies.get('userid')
    res = SendSQL("SELECT * FROM `ytuwind`.`lostandfound` WHERE `id` = '"+id+"' ")[0]
    fun.log(res)
    title = "失物招领中心"
    if str(res)=="()":
        errortext = "未知错误"
    else:
        return render_template('lostandfound.html', **locals())

@app.route('/new',methods=['POST','GET'])
def new():
    if IfLogin() == False:
        return redirect(url_for('user_login'))
    userid = request.cookies.get('userid')
    fun.log(userid)
    user_data = GetUserDateByUserId(userid)
    username = user_data[1]
    title = "发布新帖子"
    if request.method == 'POST':
        data_title = RFG('title')
        data_content = RFG('content')
        data_phonenum = RFG('phonenum')
        data_qqnum = RFG('qqnum')
        data_url = url_for('static',filename='img/default_add.jpg')
        sql = "INSERT INTO `ytuwind`.`lostandfound`(`title`, `content`, `imageurls`,`phonenum`,`qqnum`,`userid`,`username`) VALUES ('"+data_title+"', '"+data_content+"', '"+data_url+"','"+data_phonenum+"','"+data_qqnum+"','"+userid+"','"+username+"')"
        res = SendSQL(sql)
        messagetext = "发布成功"



    return render_template('new.html',**locals())
@app.route('/changeheadimg')
def changeheadimg():
    if IfLogin() == False:
        return redirect(url_for('user_login'))
    else:
        userid=request.cookies.get('userid')
    title = "修改头像"
    return render_template('changeheadimg.html',**locals())

def UploadFile(file_obj,file_path):
    if file_path==None:
        file_path='./'
    if file_obj:
        filename = str(datetime.datetime.timestamp(datetime.datetime.now())*1000000)+'.jpg'
        f = open(file_path+filename, 'wb')
        data = file_obj.read()
        f.write(data)
        f.close()
        return True

if __name__ == '__main__':
    if (app.debug == True):
        fun.log("http://127.0.0.1:5000")
        app.run(config_json['app_host'], port=config_json['app_debug_port'])
    else:
        app.run(config_json['app_host'], port=config_json['app_port'])

