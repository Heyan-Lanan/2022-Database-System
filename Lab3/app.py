import pymysql
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def register1():
    return render_template('index.html')


@app.route('/register', methods=["GET", "POST"])
def register2():
    if request.method == "GET":
        return render_template('register.html')

    username = request.form.get("User_Name")
    password = request.form.get("User_Password")
    print(username, password)

    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql1 = "insert into user(User_Name,User_Password) values(%s,%s)"

    cursor.execute(sql1, [username, password])
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/')


@app.route('/login', methods=["GET", "POST"])
def register3():
    if request.method == "GET":
        return render_template('login.html')

    username = request.form.get("User_Name")
    password = request.form.get("User_Password")

    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql1 = "select User_Password from user where User_Name = (%s)"

    cursor.execute(sql1, [username, ])
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    # print(data[0]['User_Password'], password)
    if data[0]['User_Password'] == password:
        return redirect('/user/list')
    else:
        return redirect('/login')


@app.route('/user/add', methods=["GET", "POST"])
def register4():
    if request.method == "GET":
        return render_template('user_add.html')

    username = request.form.get("User_Name")
    password = request.form.get("User_Password")
    # print(username, password)

    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql1 = "insert into user(User_Name,User_Password) values(%s,%s)"

    cursor.execute(sql1, [username, password])
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/user/list')


@app.route("/user/list")
def show_user():
    # ########## 从数据库获取所有用户信息 ###########
    # 1.连接MySQL
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 2.发送指令
    sql = "select * from user"
    cursor.execute(sql)
    data_list = cursor.fetchall()

    # 3.关闭
    cursor.close()
    conn.close()

    return render_template('user_list.html', data_list=data_list)


@app.route("/user/delete/<string:nid>")
def delete_user(nid):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "delete from user where User_Name = " + "'" + nid + "'"
    print(sql)
    cursor.execute(sql)
    conn.commit()
    # data_list = cursor.fetchall()

    # 3.关闭
    cursor.close()
    conn.close()

    return redirect('/user/list')


if __name__ == '__main__':
    app.run()
