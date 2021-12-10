import base64
import hmac
import json
import traceback
import datetime
from hashlib import md5
import time
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
                    cursor.execute(sql, (wedding_id, nickname, headshots, context, time))
                    print("有没有查询")
                db.commit()
                print("有没有提交")
            finally:
                db.close()
                print("结束了")
            message = {'status': 'success'}
        except Exception as e:
            traceback.print.exc()
            print("异常了没")
            return jsonify({'status': 'fail'})
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

# 查询有无wedding_id存在
@app.route('/findweddings',methods = ['GET'])
def find_weddings():
    # 从前端得到一个wedding_id
    data = request.values
    wedding_id = data['wedding_id']
    db = connectdb()
    c = db.cursor()
    c.execute('select wedding_id,nickname from weddings where wedding_id = %s', wedding_id)
    if c.fetchone() == None:    # 获取符合条件的第一个值的所有信息,返回结果类型为元组，如果查询不到，则返回None
        a = 0
    else:
        a = 1
    c.close()
    db.close()
    if a == 1:
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})

# 导航页
@app.route('/navigation', methods = ['GET'])
def navigator():
    data = request.values
    wedding_id = data['wedding_id']
    print(wedding_id)
    db = connectdb()
    c = db.cursor()
    c.execute('select longtitute,latitute,content from navigation where wedding_id = %s', wedding_id)
    result = c.fetchone()   #获取到经纬度和内容
    print(result)
    longtitute = result[0]
    print(longtitute)
    latitute = result[1]
    print(latitute)
    content = result[2]
    print(content)
    c.close()
    db.close()
    data = {
        "longtitute": longtitute,
        "latitute": latitute,
        "content": content
    }
    return jsonify(data)


# #获得token，key: str (用户给定的key，需要用户保存以便之后验证token,每次产生token时的key 都可以是同一个key)，expire: int(最大有效时间，单位为s)
# def generate_token(key, expire=3600):
#     ts_str = str(time.time() + expire)
#     ts_byte = ts_str.encode("utf-8")        #时间戳
#     sha1_tshexstr = hmac.new(key.encode("utf-8"),ts_byte,'sha1').hexdigest()
#     token = ts_str+':'+sha1_tshexstr
#     b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
#     return b64_token.decode("utf-8")
#
# # 验证token
# def certify_token(key, token):
#     token_str = base64.urlsafe_b64decode(token).decode('utf-8')     #解码
#     token_list = token_str.split(':')
#     if len(token_list) != 2:
#         return False
#     ts_str = token_list[0]
#     if float(ts_str) < time.time(): #判断是否过期
#     # token expired
#         return False
#     known_sha1_tsstr = token_list[1]
#     sha1 = hmac.new(key.encode("utf-8"),ts_str.encode('utf-8'),'sha1')
#     calc_sha1_tsstr = sha1.hexdigest()
#     if calc_sha1_tsstr != known_sha1_tsstr:
#     # token certification failed
#         return False
#     # token certification success
#     else:
#         return True
#
# # 登录注册
# @app.route('/login', methods = ['POST'])
# def login():
#     data = json.loads(request.get_data(as_text=True))
#     code = data['code']
#     appid = 'appID'  # 开发者关于微信小程序的appID
#     appSercet = 'appSecret'  # 开发者关于微信小程序的appSecret
#     # 向微信接口服务发送请求
#     api = 'https://api.weixin.qq.com/sns/jscode2session?appid='+appid+'&secret='+appSercet+'&js_code='+code+'&grant_type=authorization_code'
#     response_data = request.get(api)
#     resData = response_data.json()
#     openid = resData['openid']  # 得到用户关于当前小程序的OpenID
#     session_key = resData['session_key']  # 得到用户关于当前小程序的会话密钥session_key
#     # 下面生成自定义状态：token，用session_key和openid,
#     token = generate_token(openid+session_key, expire=3600)
#     message = (
#         {'status': 'fail',
#          'token':token
#         }
#     )
#     return jsonify(message)




@app.route('/')
def hello():
    return "<p>Hello, World!</p>"



if __name__ == '__main__':
    app.run()
