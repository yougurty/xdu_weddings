import json
import traceback
import random
from flask import Flask,request,jsonify
import pymysql
from messageAPI import messageAPI
from navigationAPI import navigationAPI
from invitationAPI import invitationAPI
from participantAPI import participantAPI

app = Flask(__name__)

app.register_blueprint(messageAPI)
app.register_blueprint(navigationAPI)
app.register_blueprint(invitationAPI)
app.register_blueprint(participantAPI)

def connectdb():
    print('连接到mysql服务器...')
    # 打开数据库连接
    # 用户名:hp, 密码:Hp12345.,用户名和密码需要改成你自己的mysql用户名和密码，并且要创建数据库TESTDB，并在TESTDB数据库中创建好表Student
    db = pymysql.connect(host='101.35.85.119',
                        user='root',
                        password='Xsy123456',
                        database='MInvitation')
    print('连接上了!')
    return db

# 查询有无wedding_id存在
@app.route('/weddings',methods = ['GET'])
def find_weddings():
    # 从前端得到一个wedding_id
    data = request.values
    wedding_id = data['wedding_id']
    db = connectdb()
    c = db.cursor()
    c.execute('select wedding_id,hostname from weddings where wedding_id = %s', wedding_id)
    print(wedding_id)
    temp = c.fetchone()
    print(temp)
    if temp == None:    # 获取符合条件的第一个值的所有信息,返回结果类型为元组，如果查询不到，则返回None
        a = 0
    else:
        a = 1
    c.close()
    db.close()
    print(a)
    if a == 1:
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})

#随机生成六位数的wedding_id
def generate_weddingid(isnum):
    # ''' 随机生成6位的验证码 '''
    code_list = []
    if isnum == True:
        for i in range(10):  # 0-9数字
            code_list.append(str(i))
    else:
        for i in range(10):  # 0-9数字
            code_list.append(str(i))
        for i in range(65, 91):  # A-Z
            code_list.append(chr(i))
        for i in range(97, 123):  # a-z
            code_list.append(chr(i))
    myslice = random.sample(code_list, 6)  # 从list中随机获取6个元素，作为一个片断返回
    verification_code = ''.join(myslice)  # list to string
    return verification_code

# 主人新建婚礼，要给出主人的昵称。
@app.route('/weddings', methods = ['POST'])
def create_wedding():
    if request.method == 'POST':
        post_data = json.loads(request.get_data().decode('utf-8'))
        hostname = post_data[0]['nickname']
        # 存到数据库里，然后随机生成一个wedding_id
        wedding_id = generate_weddingid(True)
        db = connectdb()
        c = db.cursor()
        c.execute('select wedding_id from weddings where wedding_id = %s', wedding_id)
        while c.fetchone() != None :
            wedding_id = generate_weddingid(True)
        # 存wedding_id和host_name到数据库中
        try:
            sql = "INSERT INTO `weddings` (`wedding_id`, `hostname`) VALUES (%s, %s)"
            c.execute(sql, (wedding_id, hostname))
            db.commit()
            print('数据提交到weddings成功')
        except Exception as e:
            traceback.print.exc()
            return jsonify({'status':'fail'})
        finally:
            db.close()
            print("结束了")
        result = (
            {
                'wedding_id': wedding_id,
                'status': 'success'
            }
        )
    return jsonify(result)




@app.route('/')
def hello():
    connectdb()

    return "<p>Hello, World!</p>"



if __name__ == '__main__':
    # from werkzeug.contrib.fixers import ProxyFix
    # app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()
