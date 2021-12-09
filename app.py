import json
import traceback
import datetime
from flask import Flask,request,jsonify
import pymysql

app = Flask(__name__)

def connectdb():
    print('连接到mysql服务器...')
    # 打开数据库连接
    # 用户名:hp, 密码:Hp12345.,用户名和密码需要改成你自己的mysql用户名和密码，并且要创建数据库TESTDB，并在TESTDB数据库中创建好表Student
    #db = pymysql.connect("101.35.85.119","root","Xsy123456.","EXP");
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='539625jsy!',
                         database='SJ')
    print('连接上了!')
    return db

# 插入一条新的留言
@app.route('/msgs', methods = ['POST'])
def addnew_msg():  # put application's code here
    global data
    if request.method == 'POST':
        try:
            print("测试")
            # post_data = request.get_json()
            # print(request.args)
            # post_data = request.values;
            # print(post_data)
            # post_data = json.loads(request.get_data(as_text=True))
            # print(post_data)
            post_data = json.loads(request.get_data().decode('utf-8'))
            wedding_id = post_data[0]['wedding_id']
            print(wedding_id)
            nickname = post_data[0]['nickname']
            headshots = post_data[0]['headshots']
            context = post_data[0]['context']
            time = datetime.datetime.now().strftime('%Y-%m-%d %T')
            print(time)
            db = connectdb()
            try:
                with db.cursor() as cursor:
                    # 创建一条新的记录
                    sql = "INSERT INTO `messages` (`wedding_id`, `nickname`,`headshots`,`context`,`time`) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(sql,(wedding_id,nickname,headshots,context,time))
                    print("有没有查询")
                db.commit()
                print("有没有提交")
            finally:
                db.close()
                print("结束了")
            message = {'status':'success'}
        except Exception as e:
            traceback.print.exc()
            print("异常了没")
            return jsonify({'status':'fail'})
        else:
            return jsonify(message)

# 获取所有留言
@app.route('/msgs', methods = ['GET'])
def get_all_msg():
    db = connectdb()
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor) # 想返回字典格式，只需要在建立游标的时候加个参数，cursor=pymysql.cursors.DictCursor。这样每行返回的值放在字典里面，然后整体放在一个list里面。
    sql = 'select * from messages'
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    db.close()
    return jsonify(result)


#
# #登录注册
@app.route('/signin', methods = ['POST'])
def signin():
    data = json.loads(request.get_data(as_text=True))
    code = data['code']
    appid = 'appID'  # 开发者关于微信小程序的appID
    appSercet = 'appSecret'  # 开发者关于微信小程序的appSecret
    api = 'https://api.weixin.qq.com/sns/jscode2session?appid='+appid+'&secret='+appSercet+'&js_code='+code+'&grant_type=authorization_code'
    request.get(api)

@app.route('/')
def hello():
    return "<p>Hello, World!</p>"



if __name__ == '__main__':
    app.run()
