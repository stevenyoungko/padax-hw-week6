from flask import Flask
from flask import request #載入 request 物件
from flask import redirect
from flask import render_template
from flask import session
import os
import json
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="website"
)

app = Flask( __name__, static_folder='static', static_url_path='/')
app.config['SECRET_KEY'] = os.urandom(24)

@app.route("/api/users")
def users():
  username = request.args.get("username", "")
  mycursor = mydb.cursor(dictionary=True)
  mycursor.execute( "SELECT * FROM user WHERE username = %s", (username,))
  myresult = mycursor.fetchone()
  if (myresult):
    value = {
      "data": {
        "id": myresult['id'],
        "name": myresult['name'],
        "username": myresult['username']
      }
    }
  else:
    value = {
      "data": None
    }
  return json.dumps(value, ensure_ascii=False)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
  name=request.form['name']
  username=request.form['username']
  password=request.form['password']
  mycursor = mydb.cursor()
  sql = "SELECT * FROM user WHERE username = %s"
  val = (username, )
  mycursor.execute(sql, val)
  myresult = mycursor.fetchall()
  if(myresult):
    return redirect('/error?message="帳號已經被註冊"')
  else:
    sql = "INSERT INTO user (name, username, passward) VALUES (%s, %s, %s)"
    val = (name, username, password)
    mycursor.execute(sql, val)
    mydb.commit()
    return redirect('/')

@app.route('/signin', methods=['POST'])
def singin():
  username=request.form['username']
  password=request.form['password']
  mycursor = mydb.cursor(dictionary=True)
  sql = "SELECT * FROM user WHERE username = %s AND passward = %s"
  val = (username, password)
  mycursor.execute(sql, val)
  myresult = mycursor.fetchone()
  print()
  if (myresult):
    session['isLogin'] = True
    session['name'] =  myresult['name']
    return redirect('/member')
  else:
    return redirect('/error?message="帳號或密碼輸入錯誤"')

@app.route('/signout')
def signout():
  session['isLogin'] = False
  return redirect('/')

@app.route('/member')
def member():
  isLogin = session.get('isLogin')
  if (isLogin):
    name = session.get('name')
    return render_template('member.html', data=name)
  else:
    return redirect('/')

@app.route('/error')
def error():
  message = request.args.get("message", "帳號或密碼輸入錯誤")
  return render_template('error.html', data=message)

app.run(port=3000)