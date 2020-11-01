from flask import Flask,render_template,request,make_response,redirect,url_for,Response
import pymysql
import os
import platform

app = Flask(__name__)

# 打开数据库连接

def SetCookie(fun,cookiename,cookietext,alivetime):
    response = redirect(url_for(fun))
    response.set_cookie(cookiename, cookietext,max_age=alivetime)  # set_cookie视图会在生成的响应报文首部中创建一个Set-Cookie字段,即"Set-Cookie: name=xxx;Path=/"
    return response
def GetCookie(cookiename):
    cookie_1 = request.cookies.get(cookiename)  # 获取名字为cookiename对应cookie的值
    return cookie_1
def DeleteCookie(fun,cookiename):
    resp = redirect(url_for(fun))
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
    arry = []
    arry.append(-1)
    arry.append(-1)
    arry.append('')
    iskong = SendSQL("SELECT * FROM `ytuwind`.`yw_users` WHERE `username` = '"+username+"' ")
    print(iskong)
    if str(iskong) != "()":
        arry[0] = 2
        arry[2]="用户名重复"
        print("用户名重复")
        return arry
    sql = \
        "INSERT INTO `ytuwind`.`yw_users`(`username`, `password`, `realname`, `studentsnum`, `college`, `major`, `headimageurl`, `phonenum`, `classnum`, `QQnum`) " \
        "VALUES ('"+username+"', '"+password+"', '"+realname+"', '"+studentnum+"', '"+college+"', '"+major+"', '"+headimageurl+"', '"+phonenum+"', '"+str(classnum)+"', '')"
    res = SendSQL(sql)
    if res == 1:
        print("注册成功")
    if res == -1:
        arry[2]=("注册失败")
        print("注册失败")
        return arry

    id = SendSQL("SELECT * FROM `ytuwind`.`yw_users` WHERE `username` = '" + username + "' ")[0][0]
    print(id)
    arry[0]=(res)
    arry[1]=(id)
    arry[2]=("注册成功")
    return arry
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
        userid = RFG('userid')
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
        # print(request.form.items())
        print(username,password,realname,studentnum,college,major,headimageurl,phonenum,classnum)
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
        print(res)
        if str(res)=="()":
            #登录失败
            messagetext="账号或密码错误"
            print("登录失败")
            return render_template('login.html',**locals())
        else:
            userid= res[0][0]
            print(userid)
            response = redirect(url_for('index'))

            response.set_cookie('username', username, max_age=3600)
            response.set_cookie('userid', str(userid), max_age=3600)
            return response
    else :
        userid = request.cookies.get("userid")
        if userid==None:#未登录
            return render_template('login.html',**locals())
        else:#已登录
            title = "首页"
            return render_template('index.html',**locals())

@app.route('/user',methods=['GET'])
def UserId():
    if request.method=='GET':
        userid=RFG('userid')
    if userid==None:
        userid = request.cookies.get('userid')
    print(userid)
    title = "我的"
    sql = "SELECT * FROM `ytuwind`.`yw_users` WHERE `id` = '"+str(userid)+"'"
    user_data = SendSQL(sql)[0]
    print(user_data)
    userid=user_data[0]
    username = user_data[1]


    return render_template('user.html',**locals())

@app.route('/function/<function>')
def softfunction(function):
    if IfLogin() == False:
        return redirect(url_for('user_login'))
    else:
        userid = RFG('userid')
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
        userid = RFG('userid')
    title = "失物招领中心"
    lostandfoundtasts = SendSQL("SELECT * FROM `ytuwind`.`lostandfound`")
    print(lostandfoundtasts)
    return render_template('lostandfoundtasts.html',**locals())
@app.route('/lostandfoundtasts/<id>')
def lostandfoundtasts_id(id):
    if IfLogin() == False:
        return redirect(url_for('user_login'))
    else:
        userid=RFG('userid')
    res = SendSQL("SELECT * FROM `ytuwind`.`lostandfound` WHERE `id` = '"+id+"' ")[0]
    print(res)
    title = "失物招领中心"
    if str(res)=="()":
        errortext = "未知错误"
    else:
        return render_template('lostandfound.html', **locals())

@app.route('/new')
def new():
    if IfLogin() == False:
        return redirect(url_for('user_login'))
    else:
        userid=RFG('userid')
    title =  "发布新帖子"
    return render_template('new.html',**locals())
@app.route('/changeheadimg')
def changeheadimg():
    if IfLogin() == False:
        return redirect(url_for('user_login'))
    else:
        userid=RFG('userid')
    title = "修改头像"
    return render_template('changeheadimg.html',**locals())

# db = pymysql.connect("localhost", "ytuwind", "XC4djtPwCDjsfGZG", "ytuwind", charset='utf8' )
db = pymysql.connect("112.124.21.126", "ytuwind", "XC4djtPwCDjsfGZG", "ytuwind", charset='utf8' )
print(db)
if __name__ == '__main__':
    sysstr = platform.system()
    if (sysstr == "Windows"):
        app.debug = True
    elif (sysstr == "Linux"):
        app.debug = False
    if (app.debug == True):
        app.run('127.0.0.1' , port=8000)
    else:

        app.run('0.0.0.0', port=5000)
