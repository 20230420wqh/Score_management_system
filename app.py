import os
#import logging
import time
from functools import wraps
from flask import Flask, request, send_file,redirect,session,render_template
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment, Font
import random
import zipfile
import mysql.connector
from datetime import datetime
from flask_session import Session
#
# mydb = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="root_wqh_linux_centOS",
#         database="expression_generator"
#   )
ip_astrict = 0
try:

    # 连接MySQL数据库
    mydb = mysql.connector.connect(
        host="47.115.200.81",
        user="root",
        password="wqh@2023",
        database="Score_management_system__teacher",
        port = 3306
    )
    cursor = mydb.cursor()
    # 如果连接成功
    if mydb.is_connected():
        print("MySQL数据库连接成功，已连接到Score_management_system__teacher")
    else:
        print("MySQL数据库连接失败!")
except mysql.connector.Error as e:
    print("错误原因：", str(e))

# def perform_database_operation():
#     # 在需要连接数据库的地方创建一个新的连接
#     with mysql.connector.connect(
#         host="47.115.200.81",
#         user="root",
#         password="wqh@2023",
#         database="Score_management_system__teacher",
#         port=3306
#     ) as mydb:
#         if mydb.is_connected():
#             print("MySQL数据库连接成功")
#             # 执行数据库操作
#             cursor = mydb.cursor()
#             cursor.execute("SELECT * FROM user")
#             result = cursor.fetchall()
#             print(result)
#             mydb.close()

#         else:
#             print("MySQL数据库连接失败")

def mysqlif():
    #判断mysql是否连接成功，如果没有成功就重连
    mydb = mysql.connector.connect(
    host="47.115.200.81",
    user="root",
    password="wqh@2023",
    database="expression_generator",
    port = 3306
        )
    if not mydb.is_connected():
        mydb = mysql.connector.connect(
        host="47.115.200.81",
        user="root",
        password="wqh@2023",
        database="expression_generator",
        port = 3306
        )
        print("连接成功（已重新连接）")
    else:
        print("连接成功")
    return mydb

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
app.secret_key = 'wqh@123#$ddaa&%'  # 替换为安全的密钥

@app.route('/')
def default_route():
    return redirect('/loginface')

@app.route('/loginface')
def login():
    session.pop('username', None)
    return app.send_static_file("login_interface.html")

@app.route('/login', methods=['POST'])
def login_post():
    # mydb = mysql.connector.connect(
    # host="47.115.200.81",
    # user="root",
    # password="wqh@2023",
    # database="expression_generator",
    # port = 3306
    #     )
    # if not mydb.is_connected():
    #     mydb = mysql.connector.connect(
    #     host="47.115.200.81",
    #     user="root",
    #     password="wqh@2023",
    #     database="expression_generator",
    #     port = 3306
    #     )
    #     print("连接成功（重新连接）")
    # else:
    #     print("连接成功")
    # perform_database_operation()
    mydb._open_connection()
    mysqlif()
    username = request.form['username']
    password = request.form['password']
    print("有人登录，用户名为：")
    print(username)
    print("密码为：")
    print(password)

    # 在数据库中查找对应账户
    mycursor = mydb.cursor()
    sql = "SELECT * FROM user WHERE username = %s AND password = %s"
    val = (username, password)
    mycursor.execute(sql, val)
    user = mycursor.fetchone()
    # 如果找到了对应账户，则登录成功
    if user:
        #logging.info("登录成功")
        print("登录成功")
        session['username'] = username  # 将用户名存储在会话中
        return redirect('/home')

    else:
        print("登录失败")
        return "登录失败，请检查用户名和密码！"
    
def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if 'username' in session:
            return view_func(*args, **kwargs)
        else:
            return redirect('/loginface')
    return wrapped_view

@app.route('/home')
@login_required
def index():
    username = session.get('username')
    return render_template('homepage.html')

@app.route('/goabout', methods=['POST'])
def index2():
    return redirect('/about')

@app.route('/about')
@login_required
def index3():
    return app.send_static_file('aboutwqh.html')

@app.route('/gohome', methods=['POST'])
def index4():    
    return redirect('/home')

@app.route('/goadd',methods=['POST'])
def index5():
    return redirect('/add')

@app.route('/add')
@login_required
def index6():
    username = session.get('username')
    return render_template('grade_add.html',username = username)
    #app.send_static_file这个是旧的路径
@app.route('/userpush')
@login_required
def userpush():
    # mydb = mysql.connector.connect(
    # host="47.115.200.81",
    # user="root",
    # password="wqh@2023",
    # database="expression_generator",
    # port = 3306
    #     )
    # if not mydb.is_connected():
    #     mydb = mysql.connector.connect(
    #     host="47.115.200.81",
    #     user="root",
    #     password="wqh@2023",
    #     database="expression_generator",
    #     port = 3306
    #     )
    #     print("连接成功（重新连接）")
    # else:
    #     print("连接成功")
    username = session.get('username')
    # if username != 'Administrator'or'amy_ad'or'wqh_ad':
    #     return redirect('/home')
    # else:
    mydb._open_connection()
    mysqlif()
    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    mydb.close()
    username = session.get('username')
    return render_template('userpush.html', users=users,username = username)

@app.route('/delete/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    if user_id == 1 or user_id == 2 or user_id ==3:
        redirect('/userpush')
    else:
        mydb._open_connection()
        # 执行删除用户的SQL语句
        delete_query = 'DELETE FROM user WHERE id = %s'
        cursor.execute(delete_query, (user_id,))
        # 提交事务
        mydb.commit()
        mydb.close()
    return redirect('/userpush')

@app.route('/applog')
@login_required
def applog():
    username = session.get('username')
    return render_template('applog.html',username = username)
    

@app.route('/logout', methods=['POST'])
def logout():
    # 清除会话中的用户信息
    session.pop('username', None)
    # 重定向到登录页面
    return redirect('/loginface')


if __name__ == '__main__':
    app.run(port=5001,host='0.0.0.0')