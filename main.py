from flask import Flask, render_template, request, url_for, make_response, jsonify, redirect, abort
import sqlite3 as sql
import time
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
@app.route('/verify', methods=['POST'])
def verify():
    return redirect(url_for('index'))

@app.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        con = sql.connect('database.db')
        try:
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

            con.execute('INSERT INTO member(name, email, password, birthday, age, gender) VALUES(?, ?, ?, ?, ?, ?)', (name, email, password, birthday, age, gender))
            con.commit()
            print('新增成功')
        except Exception as e:
            print('新增失敗')
            app.logger.error(e)
            con.rollback()
        finally:
            con.close()
            return redirect(url_for('log_in'))

@app.route('/jp')
def jp():
    return render_template('jp.html')

@app.route('/jp-list')
def jp_list():
    return render_template('jp-list.html')
