from flask import Flask, render_template, redirect, url_for, request, make_response, jsonify, abort, session
import sqlite3 as sql
import json
import os
import time
import math

from flask.helpers import flash
from flask.wrappers import Response
# db.py
import db

DB = db.DatebaseDriver()
app = Flask(__name__)
# 為了安全性, Flask 要求設定 SECRET_KEY, 才能使用 session
app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/log-in')
def log_in():
    # get session
    if 'LoggedIn' in session:
        return redirect(url_for('member'))
    return render_template('log-in.html')


@app.route('/member')
def member():
    if 'LoggedIn' in session:
        email = session['email']
        password = session['password']
        row = DB.get_member_by_login(email, password)[1]
        return render_template('member.html', row=row)
    return redirect(url_for('log_in'))


@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        new_password = request.form['password']
        if 'LoggedIn' in session:
            email = session['email']
            old_password = session['password']

            rowcount = DB.update_member_password_by_login(
                new_password, email, old_password)
            if rowcount == 1:
                password = new_password
                session['password'] = password
                msg = f"密碼已更改成功! 新密碼為：{new_password}"
            else:
                password = old_password
                msg = "更新失敗"
                return redirect('member')

            row = DB.get_member_by_login(email, password)[1]
            return render_template('member.html', row=row, msg=msg)


@app.route('/log-out', methods=['POST'])
def log_out():
    session.pop('LoggedIn', None)
    session.pop('email', None)
    session.pop('password', None)
    print(session)
    return redirect(url_for('log_in'))


@app.route('/verify', methods=['POST'])
def verify():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

    # todo 驗證帳密是否含有攻擊字元再執行SQL指令
    # Ex: "' or '1' = '1'"

    member = DB.get_member_by_login(email, password)[1]
    if member is None:
        msg = "帳號密碼有誤，請重新輸入"
        return render_template('log-in.html', msg=msg)
    else:
        # set session
        session['LoggedIn'] = True
        session['email'] = email
        session['password'] = password
        member_name = member[1]
        print(f"{member_name} 登入成功")
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

        is_member = DB.get_member_by_login(email, password)[0]
        if is_member:
            msg = "此信箱已被註冊過"
        else:
            member_id = DB.insert_member_table(
                name, email, password, birthday, age, gender)
            member = DB.get_member_by_id(member_id)
            if member is None:
                msg = "註冊失敗"
            else:
                msg = f"{member[1]} 您已註冊成功"
        return render_template('log-in.html', msg=msg)


@app.route('/jp')
def jp():
    return render_template('jp.html')


@app.route('/jp-list')
def jp_list():
    return render_template('jp-list.html')


@app.route('/message')
def message():
    n = 5
    rows = DB.get_all_messages()
    pages = math.ceil(len(rows) / n)
    rows = DB.get_message_by_page(0, n)
    return render_template('message.html', rows=rows, pages=pages)

# Ajax route


@app.route('/ajax/get_msg', methods=['GET', 'POST'])
def get_messages():
    if request.method == 'POST':
        n = 5
        rows = DB.get_all_messages()
        pages = math.ceil(len(rows) / n)
        page = int(request.json['page'])
        page = (page - 1) * n
        rows = DB.get_message_by_page(page, n)
        response = {
            "rows": rows,
            "pages": pages
        }
        return jsonify(response)


@app.route('/ajax/add_msg', methods=['POST'])
def add_message():
    if request.method == 'POST':
        response = {
            "success": False,
            "msg": "錯誤"
        }
        if 'LoggedIn' in session:
            comment = request.json['comment']
            email = session['email']
            password = session['password']
            member_id = DB.get_member_by_login(email, password)[1][0]
            message_id = DB.insert_message_table(email, comment, member_id)
            message = DB.get_message_by_id(message_id)
            response["success"] = True
            response["msg"] = "留言成功"
        else:
            response["msg"] = "請先登入才能留言"

    return jsonify(response)


@app.route('/ajax/del_msg/<int:msg_id>', methods=['DELETE'])
def del_msg(msg_id):
    if request.method == 'DELETE':
        response = {
            "success": False,
            "msg": "刪除失敗"
        }
        if 'LoggedIn' in session:
            email = session['email']
            password = session['password']
            member_id = DB.get_member_by_login(email, password)[1][0]
            DB_member_id = DB.get_message_by_id(msg_id)[3]

            if member_id == DB_member_id:
                DB.delete_message_by_id(msg_id)
                response["success"] = True
                response["msg"] = "這則回應已被刪除"
            else:
                response["msg"] = "無法刪除他人留言"
                return jsonify(response)
        else:
            response["msg"] = "請先登入才能刪除留言"
            return jsonify(response)
        return jsonify(response)
