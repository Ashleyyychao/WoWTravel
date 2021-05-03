from flask import Flask, render_template, request, url_for, make_response, jsonify, redirect, abort
import sqlite3 as sql
import json
import time
# db.py
import db

DB = db.DatebaseDriver()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log-in')
def log_in():
    # todo 已登入後要顯示會員基本資料
    return render_template('log-in.html')

@app.route('/verify', methods=['POST'])
def verify():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

    # todo 驗證帳密是否含有攻擊字元再執行SQL指令
    # Ex: "' or '1' = '1'"

    member_name = DB.get_member_name_by_login(email, password)
    if member_name is None:
        print("帳號密碼有誤，請重新輸入")
    else:
        print(f"{member_name} 歡迎回來")
        return redirect(url_for('index'))

    return redirect(url_for('log_in'))

@app.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        last_name = request.form['last_name']
        first_name = request.form['first_name']
        email = request.form['email']
        password = request.form['password']
        birthday_year = request.form['birthday_year']
        birthday_month = request.form['birthday_month']
        birthday_day = request.form['birthday_day']
        gender = request.form['gender']

        name = last_name + first_name
        birthday = birthday_year + '/' + birthday_month + '/' + birthday_day

        now = time.strftime("%Y,%m,%d")
        t = now.split(',')
        if int(t[1]) >= int(birthday_month):
            if int(t[2]) >= int(birthday_day):
                age = int(t[0]) - int(birthday_year)
        else:
            age = int(t[0]) - int(birthday_year) - 1

        # todo 驗證表單資料是否正確再放入資料庫
        # todo 驗證帳密是否含有攻擊字元再執行SQL指令

        ismember = DB.is_member(email)
        if ismember:
            print("此信箱已被註冊過")
        else:
            member_id = DB.insert_member_table(name, email, password, birthday, age, gender)

            member = DB.get_member_by_id(member_id)
            member_name = DB.get_member_name_by_login(email, password)
            if member is None:
                print("註冊失敗")
            
            print(f"{member_name} 您好! 很高興能為您服務~")
        return redirect(url_for('log_in'))

@app.route('/jp')
def jp():
    return render_template('jp.html')

@app.route('/jp-list')
def jp_list():
    return render_template('jp-list.html')