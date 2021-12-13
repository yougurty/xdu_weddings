import json
import traceback
import pymysql
from flask import Blueprint
from flask import Flask,request,jsonify

participantAPI = Blueprint('participantAPI', __name__)

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

# 获取参会人员所有信息
@participantAPI.route('/participants',methods = ['GET'])
def participant_get():
    data = request.values
    wedding_id = data['wedding_id']
    print(wedding_id)
    db = connectdb()
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)  # 想返回字典格式，只需要在建立游标的时候加个参数，cursor=pymysql.cursors.DictCursor。这样每行返回的值放在字典里面，然后整体放在一个list里面。
    sql = 'select * from participants where wedding_id = %s'
    cursor.execute(sql, wedding_id)
    result = cursor.fetchall()
    print(result)
    cursor.close()
    db.close()
    return jsonify(result)


@participantAPI.route('/participants',methods = ['POST'])
def participant_post():
    if request.method == 'POST':
        post_data = json.loads(request.get_data().decode('utf-8'))
        wedding_id = post_data[0]['wedding_id']
        phoneNumber = post_data[0]['phoneNumber']
        realName = post_data[0]['realName']
        attendance = post_data[0]['attendance']
        db = connectdb()
        c = db.cursor()
        try:
            sql = "INSERT INTO `participants` (`wedding_id`, `phoneNumber`,`realName`,`attendance`) VALUES (%s, %s, %s, %s)"
            c.execute(sql, (wedding_id, phoneNumber, realName, attendance))
            db.commit()
            print('数据提交到participants成功')
        except Exception as e:
            traceback.print.exc()
            return jsonify({'status': 'fail'})
        db.close()
        print("结束了")
        return jsonify({'status': 'success'})

