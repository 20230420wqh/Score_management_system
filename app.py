import os
import logging
import time
from functools import wraps
from flask import Flask, request, send_file,redirect,session,render_template, send_file

from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment, Font
import random
import zipfile
import mysql.connector
from datetime import datetime
from flask_session import Session
import datetime
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
        port = 3306,
        charset='utf8mb4'   # 指定字符集
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
    database="Score_management_system__teacher",
    port = 3306,
    charset='utf8mb4'   # 指定字符集
        )
    if not mydb.is_connected():
        mydb = mysql.connector.connect(
        host="47.115.200.81",
        user="root",
        password="wqh@2023",
        database="Score_management_system__teacher",
        port = 3306,
        charset='utf8mb4'   # 指定字符集
        )
        print("连接成功（已重新连接）")
    else:
        print("连接成功")
    return mydb

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
app.secret_key = 'wqh@123#$ddaa&%'  # 替换为安全的密钥

def get_next_id_of_detet():
    conn = mysql.connector.connect(
        host="47.115.200.81",
        user="root",
        password="wqh@2023",
        database="Score_management_system__teacher",
        port = 3306,
        charset='utf8mb4'   # 指定字符集
    )
    
    cursor = conn.cursor()
    select_query = "SELECT id FROM delet ORDER BY id DESC LIMIT 1"

    try:
        cursor.execute(select_query)
        result = cursor.fetchone()
        if result:
            last_id = result[0]
            next_id = last_id + 1
        else:
            next_id = 1
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        next_id = None
    finally:
        cursor.close()
        conn.close()

    return next_id

def check_condition(func):
    def wrapper(*args, **kwargs):
        # 获取用户登录的IP地址
        user_ip = request.remote_addr

        # 连接数据库
        connection = mysql.connector.connect(
        host="47.115.200.81",
        user="root",
        password="wqh@2023",
        database="Score_management_system__teacher",
        port = 3306
        )
        cursor = connection.cursor()
        appid = 'ip'
        cursor.execute("SELECT * FROM appcondition WHERE name = %s", (appid,))
        condition_data = cursor.fetchone()
        print("查询程序配置")
        print(condition_data)

        if condition_data:
            print("正在获取状态")
            condition = int(condition_data[2])
            print("正在获取状态")
            print(condition)
            if condition == 2:
                # 如果condition为2，从BlackIP表中查询IP
                cursor.execute("SELECT * FROM blackip WHERE ip = %s", (user_ip,))
                print("查询黑名单IP")
                black_ip_data = cursor.fetchone()
                if black_ip_data:
                    cursor.close()
                    connection.close()
                    return redirect('/ipsorry')

            elif condition == 3:
                cursor.execute("SELECT * FROM whiteip WHERE ip = %s", (user_ip,))
                print("查询白名单")
                white_ip_data = cursor.fetchone()
                if white_ip_data:
                    # 如果用户IP在WhiteIP表中，什么也不执行
                    cursor.close()
                    connection.close()
                    return func(*args, **kwargs)
                else:
                    return redirect("/ipsorry")
            elif condition == 1:
                print("无限制IP访问")
        cursor.close()
        connection.close()
        return func(*args, **kwargs)

    return wrapper

@app.route('/')
@check_condition
def default_route():
    return redirect('/loginface')

@app.route('/ipsorry')
def ipsorry():
    user_ip = request.remote_addr
    return render_template("ipsorry.html",user_ip=user_ip)

@app.route('/loginface', endpoint='loginface')
@check_condition
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

@app.route('/home', endpoint='home_endpoint')
@check_condition
@login_required
def home():
    username = session.get('username')
    return render_template('homepage.html',username = username)

@app.route('/downloadwhat', endpoint='downloadwhat')
@check_condition
def download():
    print("有用户下载")
    return redirect("/static/aboutapp.docx")

@app.route('/goabout', methods=['POST'])

def index2():
    return redirect('/about')

@app.route('/about', endpoint='about') 
@check_condition
@login_required
def index3():
    return app.send_static_file('aboutwqh.html')

@app.route('/gohome', methods=['POST'])

def index4():    
    return redirect('/home')

@app.route('/goadd',methods=['POST'])

def index5():
    return redirect('/add')

@app.route('/add', endpoint='addin')
@login_required
@check_condition
def index6():
    username = session.get('username')
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
    cursor.execute("SELECT * FROM pupil")
    users = cursor.fetchall()
    mydb.close()
    username = session.get('username')
    return render_template('grade_add.html', users=users,username = username)
    #app.send_static_file这个是旧的路径
@app.route('/userpush', endpoint='userpush')
@check_condition
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
    mydb._open_connection()
    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    mydb.close()
    return render_template('userpush.html', users=users,username = username)

@app.route('/delete/<int:user_id>', methods=['GET', 'POST'])

def delete_user(user_id):
    if user_id == 1 or user_id == 2 or user_id ==3:
        redirect('/userpush')
    else:
        # mydb._open_connection()
        # # 执行删除用户的SQL语句
        # delete_query = 'DELETE FROM user WHERE id = %s'
        # cursor.nextset()
        # cursor.execute(delete_query, (user_id,))
        # # 提交事务
        # mydb.commit()
        # mydb.close()
        # mydb._open_connection()
        # # 执行重新排序的SQL语句
        # reorder_query = 'SET @new_id := 0; UPDATE user SET id = @new_id := @new_id + 1 ORDER BY id;'
        # cursor.nextset()
        # cursor.execute(reorder_query)

        # # 提交重新排序事务
        # mydb.commit()
        # mydb.close()
        # 执行删除用户的SQL语句
        mydb._open_connection()  # 打开数据库连接
        cursor = mydb.cursor()  # 获取游标

        # 执行删除用户的SQL语句
        delete_query = 'DELETE FROM user WHERE id = %s'
        cursor.execute(delete_query, (user_id,))
        # 提交事务
        mydb.commit()

        # 执行重新排序的SQL语句
        cursor.execute('SET @new_id := 0')
        update_query = 'UPDATE user SET id = @new_id := @new_id + 1 ORDER BY id'
        cursor.execute(update_query)
        # 提交重新排序事务
        mydb.commit()

        mydb.close()  # 所有语句执行完成后再关闭数据库连接

    return redirect('/userpush')

@app.route('/newid', methods=['GET', 'POST'])

@login_required
def newid():
        mydb._open_connection()  # 打开数据库连接
        cursor = mydb.cursor()  # 获取游标

        # 执行重新排序的SQL语句
        cursor.execute('SET @new_id := 0')
        update_query = 'UPDATE user SET id = @new_id := @new_id + 1 ORDER BY id'
        cursor.execute(update_query)
        # 提交重新排序事务
        mydb.commit()

        mydb.close()  # 所有语句执行完成后再关闭数据库连接
        return redirect('/userpush')

@app.route('/newlist', methods=['GET', 'POST'])

@login_required
def newlist():
    return redirect('/userpush')

@app.route('/applog',endpoint='applog')
@check_condition
@login_required
def applog():
    username = session.get('username')
    return render_template('applog.html',username = username)
    
@app.route('/detelgrade',endpoint='detelgrade')
@login_required
@check_condition
def detegrade():
    username = session.get('username')
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
    cursor.execute("SELECT * FROM pupil")
    pupils = cursor.fetchall()
    mydb.close()
    username = session.get('username')
    return render_template('delgrade.html',pupils = pupils,username=username)

@app.route('/delgradepupil', methods=['POST'])
@login_required
def pushpupildel():
    options_selected = request.form.getlist('options')
    print(options_selected)
    #每个对应选项
    dif = 'Option 4'
    dif2 = 'Option 1'
    dif3 = 'Option 2'
    dif4 = 'Option 3'
    username = session.get('username')
    # mydb._open_connection()  # 打开数据库连接
    # cursor = mydb.cursor()  # 获取游标
    # insert_query = ("insert into delet (username) values (%s)")
    # par2 = (username,)
    # cursor.execute(insert_query, par2)
    # mydb.commit()
    # mydb.close()  # 所有语句执行完成后再关闭数据库连接
    current_datetime  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    week = str(datetime.datetime.today().weekday() + 1)
    name = request.form.get('pupil')
    
    mydb._open_connection()
    conn = mysql.connector.connect(
        host="47.115.200.81",
        user="root",
        password="wqh@2023",
        database="Score_management_system__teacher",
        port = 3306
        )
    cursor = conn.cursor()  # 获取游标 
    #扣分数
    delgrade = request.form.get('content')
    #后期优化
    if dif in options_selected:
        out_why = request.form.get('inputText')
        print(out_why)
        why = '其他'
        insert_query = ("insert into delet (username,name,why,week,datetime,out_why,delgrade) values (%s,%s,%s,%s,%s,%s,%s)")
        par2 = (username,name,why,week,current_datetime,out_why,delgrade)
        cursor.execute(insert_query, par2)
        # conn.commit()
    elif dif2 in options_selected:         
        why = '迟到'
        out_why = '无'
        insert_query = ("insert into delet (username,name,why,week,datetime,out_why,delgrade) values (%s,%s,%s,%s,%s,%s,%s)")
        par2 = (username,name,why,week,current_datetime,out_why,delgrade)
        cursor.execute(insert_query, par2)
        # conn.commit()
        # print("无备注")
    elif dif3 in options_selected:
        why = '午托讲话'
        out_why = '无'
        insert_query = ("insert into delet (username,name,why,week,datetime,out_why,delgrade) values (%s,%s,%s,%s,%s,%s,%s)")
        par2 = (username,name,why,week,current_datetime,out_why,delgrade)
        cursor.execute(insert_query, par2)
        # conn.commit()
    elif dif4 in options_selected:
        why = '早读讲话'
        out_why = '无'
        insert_query = ("insert into delet (username,name,why,week,datetime,out_why,delgrade) values (%s,%s,%s,%s,%s,%s,%s)")
        par2 = (username,name,why,week,current_datetime,out_why,delgrade)
        cursor.execute(insert_query, par2)
        # conn.commit()
    conn.commit()
    mydb.close()
    mydb._open_connection()
    cursor = mydb.cursor()

        # 更新指定用户名的分数
    update_query = """
        UPDATE pupil
        SET grade = grade - %s
        WHERE who = %s
    """

    cursor.execute(update_query, (delgrade, name))
    mydb.commit()  # 不要忘记提交事务来保存更改

    mydb.close() 
    # redirect('/detelgrade')
    return redirect('/newidofdel')
# @app.route('/newid')
# def mewid():
#     mydb._open_connection()
#     mysqlif()
#     with mydb.cursor() as cursor:
#             # 执行重新排序的SQL语句
#             reorder_query = 'SET @new_id := 0; UPDATE user SET id = @new_id := @new_id + 1 ORDER BY id;'
#             cursor.nextset()
#             cursor.execute(reorder_query)

#         # 提交重新排序事务
#             mydb.commit()
#     mydb.close()
#     return redirect('/userpush')

@app.route('/dellog',endpoint='dellog')
@check_condition
@login_required
def dellog():
    username = session.get('username')
    mydb._open_connection()
    conn = mysql.connector.connect(
    host="47.115.200.81",
    user="root",
    password="wqh@2023",
    database="Score_management_system__teacher",
    port = 3306,
    charset='utf8mb4'   # 指定字符集
        )
    cursor = conn.cursor()  # 获取游标
    cursor.execute("SELECT * FROM delet")
    dellog = cursor.fetchall()
    mydb.close()
    username = session.get('username')
    print(dellog)
    return render_template('dellog.html', dellogs=dellog,username = username)

@app.route('/dellogd/<int:dellog_id>', methods=['GET', 'POST'])

def delete_delet(dellog_id):
        # 执行删除用户的SQL语句
        mydb._open_connection()  # 打开数据库连接
        cursor = mydb.cursor()  # 获取游标
        select_query = 'SELECT delgrade FROM delet WHERE id = %s'
        cursor.execute(select_query, (dellog_id,))
        result = cursor.fetchone()
        if result is None:
            return "Error: No such delgrade in delet table"
        print(result)
        delgrade = result[0]

        select_query = 'SELECT name FROM delet WHERE id = %s'
        cursor.execute(select_query, (dellog_id,))
        result2 = cursor.fetchone()
        if result is None:
            return "Error: No such name in delet table"
        print(result2)
        name = result2[0]
        # 更新 pupil 表
        update_query = """
        UPDATE pupil
        SET grade = grade + %s
        WHERE who = %s
        """
        cursor.execute(update_query, (delgrade, name))

        # 执行删除用户的SQL语句
        delete_query = 'DELETE FROM delet WHERE id = %s'
        cursor.execute(delete_query, (dellog_id,))
        # 提交事务
        mydb.commit()

        # 执行重新排序的SQL语句
        cursor.execute('SET @new_id := 0')
        update_query = 'UPDATE delet SET id = @new_id := @new_id + 1 ORDER BY id'
        cursor.execute(update_query)
        # 提交重新排序事务
        mydb.commit()

        mydb.close()  # 所有语句执行完成后再关闭数据库连接

        return redirect('/dellog')

@app.route('/newdel', methods=['GET', 'POST'])

@login_required
def newdellog():
    return redirect('/dellog')

@app.route('/newidofdel', methods=['GET', 'POST'])

@login_required
def newdelid():
        # mydb._open_connection()  # 打开数据库连接
        # conn = mysql.connector.connect(
        # host="47.115.200.81",
        # user="root",
        # password="wqh@2023",
        # database="Score_management_system__teacher",
        # port = 3306
        # )
        username = session.get('username')
        if username == 'Administrator' or username == 'wqh_ad' or username == 'amy_ad':
            mydb._open_connection()
            conn = mysql.connector.connect(
            host="47.115.200.81",
                user="root",
                password="wqh@2023",
                database="Score_management_system__teacher",
                port = 3306
                )
            cursor = conn.cursor()  # 获取游标
            # 执行重新排序的SQL语句
            cursor.execute('SET @new_id := 0')
            update_query = 'UPDATE delet SET id = @new_id := @new_id + 1 ORDER BY id'
            cursor.execute(update_query)
        # 提交重新排序事务
            conn.commit()
            mydb.close()  # 所有语句执行完成后再关闭数据库连接
        else:
            print("无法更新")
        return redirect('/dellog')

@app.route('/pulldate',endpoint='pulldate')
@check_condition
@login_required
def pulldate():
    username = session.get('username')
    return render_template('downdate.html',username=username)

@app.route('/ipcondition',endpoint='ipcondition')
@check_condition
@login_required
def ipcondition():
    username = session.get('username')
    mydb._open_connection()
    cursor.execute("SELECT * FROM blackip")
    blackip = cursor.fetchall()
    mydb.close()
    mydb._open_connection()
    cursor.execute("SELECT * FROM whiteip")
    whiteip = cursor.fetchall()
    mydb.close()
    client_ip = request.remote_addr
    return render_template('ipcondition.html',username=username,blackips=blackip,whiteips=whiteip,client_ip=client_ip)

@app.route('/logout', methods=['POST'])
def logout():
    # 清除会话中的用户信息
    session.pop('username', None)
    # 重定向到登录页面
    return redirect('/loginface')


if __name__ == '__main__':
    app.run(port=5001,host='0.0.0.0')