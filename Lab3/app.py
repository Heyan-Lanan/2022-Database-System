import copy
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

    sql = "select * from user where User_Name = %s"
    sql1 = "insert into user(User_Name,User_Password) values(%s,%s)"

    cursor.execute(sql, [username])
    data = cursor.fetchall()
    if data:
        return render_template('register.html', error="The username already exists.")

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

    sql = "select * from user where User_Name = %s"

    cursor.execute(sql, [username, ])
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    if not data:
        error1 = "The username you entered does not exist."
        return render_template('login.html', error1=error1)

    if data[0]['User_Password'] == password:
        return redirect('/user/list')
    else:
        error2 = "Wrong password."
        return render_template('login.html', error2=error2)


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


@app.route("/client/list", methods=["GET", "POST"])  # todo
def client_list(**kwargs):
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

    if request.method == "POST":
        Client_ID = request.form.get("Client_ID")
        Client_Name = request.form.get("Client_Name")
        Client_Tel = request.form.get("Client_Tel")
        Client_Address = request.form.get("Client_Address")
        if Client_ID:
            data_list = list(filter(lambda x: x['Client_ID'] == Client_ID, data_list))
        if Client_Name:
            data_list = list(filter(lambda x: x['Client_Name'] == Client_Name, data_list))
        if Client_Tel:
            data_list = list(filter(lambda x: x['Client_Tel'] == Client_Tel, data_list))
        if Client_Address:
            data_list = list(filter(lambda x: x['Client_Address'] == Client_Address, data_list))

    if "error1" in kwargs.keys() or "error2" in kwargs.keys():
        return data_list
    else:
        error1 = ""
        error2 = ""
        return render_template('client_list.html', data_list=data_list, error1=error1, error2=error2)


@app.route("/account/list", methods=["GET", "POST"])
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

    if request.method == "POST":
        Account_ID = request.form.get("Account_ID")
        Bank_Name = request.form.get("Bank_Name")
        Balance = request.form.get("Balance")
        if Account_ID:
            data_list = list(filter(lambda x: x['Account_ID'] == Account_ID, data_list))
        if Bank_Name:
            data_list = list(filter(lambda x: x['Bank_Name'] == Bank_Name, data_list))
        if Balance:
            data_list = list(filter(lambda x: x['Balance'] == float(Balance), data_list))

    return render_template('account_list.html', data_list=data_list, data_list1=data_list1, data_list2=data_list2,
                           data_list3=data_list3)


@app.route("/loan/list", methods=["GET", "POST"])  # todo
def loan_list(**kwargs):
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

    if request.method == "POST":
        Loan_ID = request.form.get("Loan_ID")
        Bank_Name = request.form.get("Bank_Name")
        Loan_Amount = request.form.get("Loan_Amount")
        Loan_Status = request.form.get("Loan_Status")
        Pay_already = request.form.get("Pay_already")
        if Loan_ID:
            data_list = list(filter(lambda x: x['Loan_ID'] == Loan_ID, data_list))
        if Bank_Name:
            data_list = list(filter(lambda x: x['Bank_Name'] == Bank_Name, data_list))
        if Loan_Amount:
            # print(Loan_Amount)
            # for item in data_list:
            #     print(item)
            data_list = list(filter(lambda x: x['Loan_Amount'] == float(Loan_Amount), data_list))

        if Loan_Status:
            data_list = list(filter(lambda x: x['Loan_Status'] == Loan_Status, data_list))
        if Pay_already:
            data_list = list(filter(lambda x: x['Pay_already'] == float(Pay_already), data_list))

    if "error1" in kwargs.keys():
        return data_list, data_list2
    else:
        error1 = ""
        return render_template('loan_list.html', data_list=data_list, data_list2=data_list2, error1=error1)


@app.route("/business/list")
def business_list():
    def get_year(date):
        return date.year

    def get_month(date):
        return str(date.year) + "-" + str(date.month)

    def get_quarter(date):
        return str(date.year) + "-" + str(int((date.month - 1) / 3) + 1)

    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from account"
    sql2 = "select * from loan"
    cursor.execute(sql)
    data_list = cursor.fetchall()
    cursor.execute(sql2)
    data_list2 = cursor.fetchall()
    cursor.close()
    conn.close()

    # 处理bank
    bank_dic = {}
    for item in data_list:
        if item["Bank_Name"] in bank_dic.keys():
            bank_dic[item["Bank_Name"]].append({"date": item["Opening_Date"], "balance": item["Balance"]})
        else:
            bank_dic[item["Bank_Name"]] = [{"date": item["Opening_Date"], "balance": item["Balance"]}]

    bank_balance_year = {}
    bank_balance_quarter = {}
    bank_balance_month = {}
    list1 = []
    list2 = []
    list3 = []
    for item in bank_dic:
        list1 = bank_dic[item]
        list1 = pd.DataFrame(list1)
        list2 = copy.deepcopy(list1)
        list3 = copy.deepcopy(list1)

        list1["date"] = list1["date"].apply(get_year)
        data_dict = list1.groupby('date').balance.apply(list).to_dict()
        for key in data_dict.keys():
            data_dict[key] = sum(data_dict[key])
        bank_balance_year[item] = data_dict

        list2["date"] = list2["date"].apply(get_quarter)
        data_dict2 = list2.groupby('date').balance.apply(list).to_dict()
        for key in data_dict2.keys():
            data_dict2[key] = sum(data_dict2[key])
        bank_balance_quarter[item] = data_dict2

        list3["date"] = list3["date"].apply(get_month)
        data_dict3 = list3.groupby('date').balance.apply(list).to_dict()
        for key in data_dict3.keys():
            data_dict3[key] = sum(data_dict3[key])
        bank_balance_month[item] = data_dict3

    # 处理loan
    loan_dic = {}
    for item in data_list2:
        if item["Bank_Name"] in loan_dic.keys():
            loan_dic[item["Bank_Name"]].append({"date": item["Opening_Date"], "balance": item["Loan_Amount"]})
        else:
            loan_dic[item["Bank_Name"]] = [{"date": item["Opening_Date"], "balance": item["Loan_Amount"]}]

    loan_balance_year = {}
    loan_balance_quarter = {}
    loan_balance_month = {}
    list1 = []
    list2 = []
    list3 = []
    for item in loan_dic:
        list1 = loan_dic[item]
        list1 = pd.DataFrame(list1)
        list2 = copy.deepcopy(list1)
        list3 = copy.deepcopy(list1)

        list1["date"] = list1["date"].apply(get_year)
        data_dict = list1.groupby('date').balance.apply(list).to_dict()
        for key in data_dict.keys():
            data_dict[key] = sum(data_dict[key])
        loan_balance_year[item] = data_dict

        list2["date"] = list2["date"].apply(get_quarter)
        data_dict2 = list2.groupby('date').balance.apply(list).to_dict()
        for key in data_dict2.keys():
            data_dict2[key] = sum(data_dict2[key])
        loan_balance_quarter[item] = data_dict2

        list3["date"] = list3["date"].apply(get_month)
        data_dict3 = list3.groupby('date').balance.apply(list).to_dict()
        for key in data_dict3.keys():
            data_dict3[key] = sum(data_dict3[key])
        loan_balance_month[item] = data_dict3

    return render_template('business_list.html',
                           bank_balance_year=bank_balance_year,
                           bank_balance_quarter=bank_balance_quarter,
                           bank_balance_month=bank_balance_month,
                           loan_balance_year=loan_balance_year,
                           loan_balance_quarter=loan_balance_quarter,
                           loan_balance_month=loan_balance_month
                           )


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

    if not Client_ID:
        return render_template('client_add.html', error="Client_ID cannot be null.")
    if not Client_Name:
        return render_template('client_add.html', error1="Client_Name cannot be null.")

    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "select * from client where Client_ID = %s"
    cursor.execute(sql, [Client_ID])
    data = cursor.fetchall()
    if data:
        return render_template('client_add.html', error="The Client_ID you entered already exist.")

    sql1 = "insert into client(Client_ID, Client_Name, Client_Tel, Client_Address) values(%s, %s, %s, %s)"
    sql2 = "insert into contact(Client_ID, Contact_Name, Contact_Email, Contact_Tel, Relation) values(%s, %s, %s, %s, %s)"

    cursor.execute(sql1, [Client_ID, Client_Name, Client_Tel, Client_Address])
    conn.commit()
    cursor.execute(sql2, [Client_ID, Contact_Name, Contact_Email, Contact_Tel, Relation])
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/client/list')


@app.route("/client/delete/<string:nid>")  # todo
def delete_client(nid):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql1 = "delete from contact where Client_ID = " + "'" + nid + "'"
    sql2 = "delete from client where Client_ID = " + "'" + nid + "'"
    sql3 = "select * from own where Client_ID = %s"
    sql4 = "select * from pay where Client_ID = %s"

    cursor.execute(sql3, [nid])
    data1 = cursor.fetchall()
    cursor.execute(sql4, [nid])
    data2 = cursor.fetchall()

    error1 = ""
    error2 = ""
    if data1:
        error1 = "The client " + str(nid) + " has an account record and is not allowed to be deleted."
    if data2:
        error2 = "The client " + str(nid) + " has a loan record and is not allowed to be deleted."
    if data1 or data2:
        data_list = client_list(error1=error1, error2=error2)
        return render_template('client_list.html', data_list=data_list, error1=error1, error2=error2)

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


@app.route('/account/add/<string:nid>', methods=["GET", "POST"])  # todo
def account_add(nid):
    if request.method == "GET":
        return render_template('account_add.html')

    Account_ID = request.form.get("Account_ID")
    Bank_Name = request.form.get("Bank_Name")
    Balance = request.form.get("Balance")
    Opening_Date = request.form.get("Opening_Date")
    Account_Type = request.form.get("Account_Type")

    error1 = ""
    error2 = ""
    if not Account_ID:
        error1 = "Account_ID cannot be null."
    if not Bank_Name:
        error2 = "Bank_Name cannot be null."
    if error1 or error2:
        return render_template('account_add.html', error1=error1, error2=error2)

    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql2 = "select * from account where Account_ID = %s"
    cursor.execute(sql2, [Account_ID])
    data = cursor.fetchall()
    if data:
        return render_template('account_add.html', error1="The Account_ID you entered already exist.")

    sql3 = "select * from bank where Bank_Name = %s"
    cursor.execute(sql3, [Bank_Name])
    data2 = cursor.fetchall()
    if not data2:
        return render_template('account_add.html', error2="The Bank_Name you entered does not exist.")

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


@app.route('/loan/add', methods=["GET", "POST"])  # todo
def loan_add():
    if request.method == "GET":
        return render_template('loan_add.html')

    Loan_ID = request.form.get("Loan_ID")
    Bank_Name = request.form.get("Bank_Name")
    Loan_Amount = request.form.get("Loan_Amount")
    Loan_Status = 0
    Pay_already = 0.0

    error1 = ""
    error2 = ""
    error3 = ""
    if not Loan_ID:
        error1 = "Loan_ID cannot be null."
    if not Bank_Name:
        error2 = "Bank_Name cannot be null."
    if not Loan_Amount:
        error3 = "Loan_Amount cannot be null."
    if error1 or error2 or error3:
        print(error1)
        return render_template('loan_add.html', error1=error1, error2=error2, error3=error3)

    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql2 = "select * from loan where Loan_ID = %s"
    cursor.execute(sql2, [Loan_ID])
    data = cursor.fetchall()
    if data:
        return render_template('loan_add.html', error1="The Loan_ID you entered already exist.")

    sql3 = "select * from bank where Bank_Name = %s"
    cursor.execute(sql3, [Bank_Name])
    data2 = cursor.fetchall()
    if not data2:
        return render_template('loan_add.html', error2="The Bank_Name you entered does not exist.")

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
        conn.commit()  # todo
    else:
        error1 = "The loan " + str(nid) + " is being disbursed and is not allowed to be deleted."
        data_list, data_list2 = loan_list(error1=error1)
        return render_template('loan_list.html', data_list=data_list, data_list2=data_list2, error1=error1)

    cursor.close()
    conn.close()

    return redirect('/loan/list')


@app.route('/pay/add', methods=["GET", "POST"])  # todo
def pay_add():
    if request.method == "GET":
        return render_template('pay_add.html')

    Client_ID = request.form.get("Client_ID")
    Loan_ID = request.form.get("Loan_ID")
    Pay_ID = request.form.get("Pay_ID")
    Pay_Amount = request.form.get("Pay_Amount")
    Pay_Date = request.form.get("Pay_Date")

    error1 = ""
    error2 = ""
    error3 = ""
    error4 = ""
    if not Client_ID:
        error1 = "Client_ID cannot be null."
    if not Loan_ID:
        error2 = "Loan_ID cannot be null."
    if not Pay_ID:
        error3 = "Pay_ID cannot be null."
    if not Pay_Amount:
        error4 = "Pay_Amount cannot be null."
    if error1 or error2 or error3 or error4:
        return render_template('pay_add.html', error1=error1, error2=error2, error3=error3, error4=error4)

    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "select * from pay where Client_ID = %s and Loan_ID = %s and Pay_ID = %s"
    cursor.execute(sql, [Client_ID, Loan_ID, Pay_ID])
    data = cursor.fetchall()
    if data:
        return render_template('pay_add.html', error3="The (Client_ID, Loan_ID, Pay_ID) you entered already exist.")

    sql3 = "select * from client where Client_ID = %s"
    sql4 = "select * from loan where Loan_ID = %s"
    cursor.execute(sql3, [Client_ID])
    data3 = cursor.fetchall()
    cursor.execute(sql4, [Loan_ID])
    data4 = cursor.fetchall()

    if not data3:
        error1 = "The Client_ID you entered does not exist."
    if not data4:
        error2 = "The Loan_ID you entered does not exist."
    if error1 or error2:
        return render_template('pay_add.html', error1=error1, error2=error2)

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
