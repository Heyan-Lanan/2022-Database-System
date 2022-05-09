import datetime
import pandas as pd
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


@app.route("/user/list", methods=["GET", "POST"])
def show_user():
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    if request.method == "GET":

        sql = "select * from user"
        cursor.execute(sql)
        data_list = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('user_list.html', data_list=data_list)

    User_Name = request.form.get("User_Name")
    print(User_Name)
    sql = "select * from user where User_Name = %s"
    print(sql)

    cursor.execute(sql, [User_Name])
    data_list = cursor.fetchall()
    print(data_list)

    cursor.close()
    conn.close()

    return render_template('user_list.html', data_list=data_list)


@app.route("/department/list")
def department_list():
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from department"
    cursor.execute(sql)
    data_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('department_list.html', data_list=data_list)


@app.route("/bank/list")
def bank_list():
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from bank"
    cursor.execute(sql)
    data_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('bank_list.html', data_list=data_list)


@app.route("/employee/list")
def employee_list():
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from employee"
    cursor.execute(sql)
    data_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('employee_list.html', data_list=data_list)


@app.route("/client/list")
def client_list():
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql1 = "select * from client"
    cursor.execute(sql1)
    data_list1 = cursor.fetchall()
    sql2 = "select * from contact"
    cursor.execute(sql2)
    data_list2 = cursor.fetchall()
    cursor.close()
    conn.close()

    all_data = data_list1 + data_list2
    d = {}
    for item in all_data:
        name = item["Client_ID"]
        if name in d:
            d[name].update(item)
        else:
            d[name] = item
    data_list = []
    for k, v in d.items():
        data_list.append(v)
    return render_template('client_list.html', data_list=data_list)


@app.route("/account/list")
def account_list():
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from account"
    sql1 = "select * from checking_account"
    sql2 = "select * from saving_account"
    sql3 = "select * from own"
    cursor.execute(sql)
    data_list = cursor.fetchall()
    cursor.execute(sql1)
    data_list1 = cursor.fetchall()
    cursor.execute(sql2)
    data_list2 = cursor.fetchall()
    cursor.execute(sql3)
    data_list3 = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('account_list.html', data_list=data_list, data_list1=data_list1, data_list2=data_list2,
                           data_list3=data_list3)


@app.route("/loan/list")
def loan_list():
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from loan"
    sql2 = "select * from pay"

    cursor.execute(sql)
    data_list = cursor.fetchall()
    cursor.execute(sql2)
    data_list2 = cursor.fetchall()

    for item in data_list:
        status = item.pop('Loan_Status')
        if status == 0:
            item["Loan_Status"] = "Not issued"
        elif status == 1:
            item["Loan_Status"] = "Being issued"
        else:
            item["Loan_Status"] = "Issued"

    cursor.close()
    conn.close()
    return render_template('loan_list.html', data_list=data_list, data_list2=data_list2)


@app.route("/business/list")
def business_list():
    def get_year(date):
        return date.year

    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from account"
    cursor.execute(sql)
    data_list = cursor.fetchall()

    bank_dic = {}
    for item in data_list:
        if item["Bank_Name"] in bank_dic.keys():
            bank_dic[item["Bank_Name"]].append({"date": item["Opening_Date"], "balance": item["Balance"]})
        else:
            bank_dic[item["Bank_Name"]] = [{"date": item["Opening_Date"], "balance": item["Balance"]}]

    bank_balance_year = {}
    for item in bank_dic:
        list1 = bank_dic[item]
        list1 = pd.DataFrame(list1)

        list1["date"] = list1["date"].apply(get_year)

        data_dict = list1.groupby('date').balance.apply(list).to_dict()
        for key in data_dict.keys():
            data_dict[key] = sum(data_dict[key])
        bank_balance_year[item] = data_dict
    print(bank_balance_year)

    cursor.close()
    conn.close()
    return render_template('business_list.html', bank_balance_year=bank_balance_year)


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


@app.route("/user/delete/<string:nid>")
def delete_user(nid):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "delete from user where User_Name = " + "'" + nid + "'"
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/user/list')


@app.route("/user/edit/<string:nid>", methods=["GET", "POST"])
def update_user(nid):
    if request.method == "GET":
        conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        sql = "delete from user where User_Name = " + "'" + nid + "'"

        cursor.execute(sql)
        conn.commit()

        cursor.close()
        conn.close()
        return render_template('user_edit.html')

    username = nid
    password = request.form.get("User_Password")

    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql1 = "insert into user(User_Name,User_Password) values(%s,%s)"

    cursor.execute(sql1, [username, password])
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/user/list')


@app.route('/client/add', methods=["GET", "POST"])
def client_add():
    if request.method == "GET":
        return render_template('client_add.html')

    Client_ID = request.form.get("Client_ID")
    Client_Name = request.form.get("Client_Name")
    Client_Tel = request.form.get("Client_Tel")
    Client_Address = request.form.get("Client_Address")
    Contact_Name = request.form.get("Contact_Name")
    Contact_Email = request.form.get("Contact_Email")
    Contact_Tel = request.form.get("Contact_Tel")
    Relation = request.form.get("Relation")

    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql1 = "insert into client(Client_ID, Client_Name, Client_Tel, Client_Address) values(%s, %s, %s, %s)"
    sql2 = "insert into contact(Client_ID, Contact_Name, Contact_Email, Contact_Tel, Relation) values(%s, %s, %s, %s, %s)"

    cursor.execute(sql1, [Client_ID, Client_Name, Client_Tel, Client_Address])
    conn.commit()
    cursor.execute(sql2, [Client_ID, Contact_Name, Contact_Email, Contact_Tel, Relation])
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/client/list')


@app.route("/client/delete/<string:nid>")
def delete_client(nid):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql1 = "delete from contact where Client_ID = " + "'" + nid + "'"
    sql2 = "delete from client where Client_ID = " + "'" + nid + "'"

    cursor.execute(sql1)
    conn.commit()
    cursor.execute(sql2)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/client/list')


@app.route("/client/edit/<string:nid>", methods=["GET", "POST"])
def client_edit(nid):
    if request.method == "GET":
        return render_template('client_edit.html')

    Client_ID = nid
    Client_Name = request.form.get("Client_Name")
    Client_Tel = request.form.get("Client_Tel")
    Client_Address = request.form.get("Client_Address")
    Contact_Name = request.form.get("Contact_Name")
    Contact_Email = request.form.get("Contact_Email")
    Contact_Tel = request.form.get("Contact_Tel")
    Relation = request.form.get("Relation")

    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql1 = "update client set Client_Name = %s, Client_Tel = %s, Client_Address = %s where Client_ID = %s"
    sql2 = "update contact set Contact_Name = %s, Contact_Email = %s, Contact_Tel = %s, Relation = %s where Client_ID = %s"

    cursor.execute(sql1, [Client_Name, Client_Tel, Client_Address, Client_ID])
    conn.commit()
    cursor.execute(sql2, [Contact_Name, Contact_Email, Contact_Tel, Relation, Client_ID])
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/client/list')


@app.route('/account/add/<string:nid>', methods=["GET", "POST"])
def account_add(nid):
    if request.method == "GET":
        return render_template('account_add.html')

    Account_ID = request.form.get("Account_ID")
    Bank_Name = request.form.get("Bank_Name")
    Balance = request.form.get("Balance")
    Opening_Date = request.form.get("Opening_Date")
    Account_Type = request.form.get("Account_Type")

    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql1 = "insert into account(Account_ID, Bank_Name, Balance, Opening_Date) values(%s, %s, %s, %s)"
    cursor.execute(sql1, [Account_ID, Bank_Name, Balance, Opening_Date])
    conn.commit()

    sql = "insert into own(Client_ID, Visited_Date, Account_ID) values(%s, %s, %s)"
    cursor.execute(sql, [nid, datetime.datetime.now().strftime('%Y-%m-%d'), Account_ID])
    conn.commit()

    # print(Account_Type)
    if Account_Type == "Saving":
        Interest_Rate = request.form.get("Interest_Rate")
        Currency_Type = request.form.get("Currency_Type")
        sql2 = "insert into saving_account(Account_ID, Interest_Rate, Currency_Type) values(%s, %s, %s)"
        cursor.execute(sql2, [Account_ID, Interest_Rate, Currency_Type])
        conn.commit()
    else:
        Overdraft = request.form.get("Overdraft")
        sql2 = "insert into checking_account(Account_ID, Overdraft) values(%s, %s)"
        cursor.execute(sql2, [Account_ID, Overdraft])
        conn.commit()

    cursor.close()
    conn.close()

    return redirect('/account/list')


@app.route("/account/delete/<string:nid>")
def delete_account(nid):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql1 = "delete from saving_account where Account_ID = %s"
    sql2 = "delete from checking_account where Account_ID = %s"
    sql3 = "delete from own where Account_ID = %s"
    sql4 = "delete from account where Account_ID = %s"

    cursor.execute(sql1, nid)
    conn.commit()
    cursor.execute(sql2, nid)
    conn.commit()
    cursor.execute(sql3, nid)
    conn.commit()
    cursor.execute(sql4, nid)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/account/list')


@app.route("/account/edit/<string:nid>", methods=["GET", "POST"])
def account_edit(nid):
    if request.method == "GET":
        return render_template('account_edit.html')

    Account_ID = nid
    Visited_Date = request.form.get("Visited_Date")
    Account_Type = request.form.get("Account_Type")

    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql1 = "update own set Visited_Date = %s where Account_ID = %s"
    cursor.execute(sql1, [Visited_Date, Account_ID])
    conn.commit()

    if Account_Type == "Saving":
        Interest_Rate = request.form.get("Interest_Rate")
        Currency_Type = request.form.get("Currency_Type")
        sql2 = "update saving_account set Interest_Rate = %s, Currency_Type = %s where Account_ID = %s"
        cursor.execute(sql2, [Interest_Rate, Currency_Type, Account_ID])
        conn.commit()
    else:
        Overdraft = request.form.get("Overdraft")
        sql2 = "update checking_account set Overdraft = %s where Account_ID = %s"
        cursor.execute(sql2, [Overdraft, Account_ID])
        conn.commit()

    cursor.close()
    conn.close()

    return redirect('/account/list')


@app.route('/loan/add', methods=["GET", "POST"])
def loan_add():
    if request.method == "GET":
        return render_template('loan_add.html')

    Loan_ID = request.form.get("Loan_ID")
    Bank_Name = request.form.get("Bank_Name")
    Loan_Amount = request.form.get("Loan_Amount")
    Loan_Status = 0
    Pay_already = 0.0
    # print(type(Loan_Status))

    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql1 = "insert into loan(loan_id, bank_name, loan_amount, loan_status, pay_already) values(%s, %s, %s, %s, %s)"

    cursor.execute(sql1, [Loan_ID, Bank_Name, Loan_Amount, Loan_Status, Pay_already])
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/loan/list')


@app.route("/loan/delete/<string:nid>")
def loan_delete(nid):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql1 = "select Loan_Status from loan where Loan_ID = %s"

    cursor.execute(sql1, nid)
    data = cursor.fetchall()
    if data[0]["Loan_Status"] != 1:
        # print("ok")
        sql2 = "delete from loan where Loan_ID = %s"
        cursor.execute(sql2, nid)
        conn.commit()

    cursor.close()
    conn.close()

    return redirect('/loan/list')


@app.route('/pay/add', methods=["GET", "POST"])
def pay_add():
    if request.method == "GET":
        return render_template('pay_add.html')

    Client_ID = request.form.get("Client_ID")
    Loan_ID = request.form.get("Loan_ID")
    Pay_ID = request.form.get("Pay_ID")
    Pay_Amount = request.form.get("Pay_Amount")
    Pay_Date = request.form.get("Pay_Date")

    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql1 = "insert into pay(client_id, loan_id, pay_id, pay_amount, pay_date) values(%s, %s, %s, %s, %s)"
    sql2 = "select * from loan where Loan_ID = %s"
    sql3 = "update loan set Loan_Status = %s, Pay_already = %s where Loan_ID = %s"

    cursor.execute(sql1, [Client_ID, Loan_ID, Pay_ID, Pay_Amount, Pay_Date])
    conn.commit()
    cursor.execute(sql2, Loan_ID)
    datalist = cursor.fetchall()
    data = datalist[0]
    data_Pay_already = float(data["Pay_already"])
    data_Loan_Amount = float(data["Loan_Amount"])
    data_Pay_already += float(Pay_Amount)
    data["Loan_Status"] = 1
    if data_Pay_already == data_Loan_Amount:
        data["Loan_Status"] = 2
    cursor.execute(sql3, [data["Loan_Status"], data_Pay_already, Loan_ID])
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/loan/list')


@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
