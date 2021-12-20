import json
import traceback
import pymysql
from flask import Blueprint
from flask import Flask,request,jsonify

invitationAPI = Blueprint('invitationAPI', __name__)

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

# 获取邀请函的链接
@invitationAPI.route('/invitations',methods = ['GET'])
def invitation_get():
    data = request.values
    wedding_id = data['wedding_id']
    print(wedding_id)
    db = connectdb()
    c = db.cursor()
    try:
        c.execute('select invitationUrl from invitations where wedding_id = %s', wedding_id)
        result = c.fetchone()  # 获取到邀请函链接
        print(result)
        invitationUrl = result[0]
        print(invitationUrl)
    except Exception as e:
        traceback.print.exc()
        return jsonify({'status': 'fail'})
    c.close()
    db.close()
    data = {
        "status": "success",
        "wedding_id": wedding_id,
        "invitationUrl": invitationUrl
    }
    return jsonify(data)

@invitationAPI.route('/invitations',methods = ['POST'])
def invitation_post():
    if request.method == 'POST':
        post_data = json.loads(request.get_data().decode('utf-8'))
        invitationUrl = post_data[0]['invitationUrl']
        wedding_id = post_data[0]['wedding_id']
        db = connectdb()
        c = db.cursor()
        try:
            sql = "INSERT INTO `invitations` (`wedding_id`, `invitationUrl`) VALUES (%s, %s)"
            c.execute(sql, (wedding_id, invitationUrl))
            db.commit()
            print('数据提交到invitations成功')
        except Exception as e:
            traceback.print.exc()
            return jsonify({'status': 'fail'})
        db.close()
        print("结束了")
        return jsonify({'status': 'success'})

# 更新邀请函信息
@invitationAPI.route('/invitations', methods = ['PUT'])
def participant_put():
    if request.method == 'PUT':
        put_data = json.loads(request.get_data().decode('utf-8'))
        invitationUrl = put_data[0]['invitationUrl']
        wedding_id = put_data[0]['wedding_id']
        db = connectdb()
        c = db.cursor()
        try:
            c.execute('update invitations set invitationUrl=%s where wedding_id=%s', (invitationUrl, wedding_id))
            db.commit()
            print('数据update到invitations成功')
        except Exception as e:
            traceback.print.exc()
            return jsonify({'status': 'fail'})
        c.close()
        db.close()
        return jsonify({'status': 'success'})