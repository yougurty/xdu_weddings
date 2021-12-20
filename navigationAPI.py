import json
import traceback
import pymysql
from flask import Blueprint
from flask import Flask,request,jsonify


navigationAPI = Blueprint('navigationAPI', __name__)

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

@navigationAPI.route('/navigation', methods = ['GET'])
def navigator_get():
    data = request.values
    wedding_id = data['wedding_id']
    print(wedding_id)
    db = connectdb()
    c = db.cursor()
    c.execute('select longitude,latitude,content from navigation where wedding_id = %s', wedding_id)
    result = c.fetchone()   #获取到经纬度和内容
    print(result)
    longitude = result[0]
    print(longitude)
    latitude = result[1]
    print(latitude)
    content = result[2]
    print(content)
    c.close()
    db.close()
    data = {
        "longitude": longitude,
        "latitude": latitude,
        "content": content
    }
    return jsonify(data)

@navigationAPI.route('/navigation', methods = ['POST'])
def navigator_post():
    if request.method == 'POST':
        post_data = json.loads(request.get_data().decode('utf-8'))
        longitude = post_data[0]['longitude']
        latitude = post_data[0]['latitude']
        content = post_data[0]['content']
        wedding_id = post_data[0]['wedding_id']
        db = connectdb()
        c = db.cursor()
        try:
            sql = "INSERT INTO `navigation` (`wedding_id`, `longitude`,`latitude`,`content`) VALUES (%s, %s, %s, %s)"
            c.execute(sql, (wedding_id, longitude, latitude, content))
            db.commit()
            print('数据提交到navigation成功')
        except Exception as e:
            traceback.print.exc()
            return jsonify({'status': 'fail'})
        db.close()
        print("结束了")
        return jsonify({'status': 'success'})

# 可以改
@navigationAPI.route('/navigation', methods = ['PUT'])
def navigator_put():
    if request.method == 'PUT':
        put_data = json.loads(request.get_data().decode('utf-8'))
        longitude = put_data[0]['longitude']
        latitude = put_data[0]['latitude']
        content = put_data[0]['content']
        wedding_id = put_data[0]['wedding_id']
        db = connectdb()
        c = db.cursor()
        try:
            c.execute('update navigation set longitude=%s,latitude=%s,content=%s where wedding_id=%s', (longitude,latitude,content,wedding_id))
            db.commit()
            print('数据update到navigation成功')
        except Exception as e:
            traceback.print.exc()
            return jsonify({'status': 'fail'})
        c.close()
        db.close()
        return jsonify({'status': 'success'})

