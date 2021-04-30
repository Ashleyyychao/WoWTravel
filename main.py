from flask import Flask, render_template, request, url_for, make_response, jsonify, redirect, abort
import sqlite3 as sql
app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = os.getcwd()+'/media'
# print(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log-in')
def log_in():
    return render_template('log-in.html')

# todo 驗證帳號密碼是否在資料庫中
# @app.route('/log-in', methods=['POST'])
# def verify():
#     pass

@app.route('/log-in', methods=['POST'])
def create():
    if request.method == 'POST':
        con = sql.connect('database.db')
        try:
            email = request.form['email']
            password = request.form['password']

            # todo 驗證是否有此Email
            email = email if len(email) else None
            if email is None:
                raise Exception('帳號不可為空')

            # todo 密碼需有大寫字母 字元不可重複3次
            password = password if len(password) else None
            if password is None:
                raise Exception('密碼不可為空')

            con.execute('INSERT INTO account(email, password) VALUES(?, ?)', (email, password))
            con.commit()
            print('新增成功')
        except Exception as e:
            print('新增失敗')
            app.logger.error(e)
            con.rollback()
        finally:
            con.close()
            return render_template('log-in.html')

@app.route('/jp')
def jp():
    return render_template('jp.html')

@app.route('/jp-list')
def jp_list():
    return render_template('jp-list.html')
