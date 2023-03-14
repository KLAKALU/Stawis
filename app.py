from flask import Flask
from flask import render_template, request, redirect, flash, url_for
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_sqlalchemy import SQLAlchemy
import codecs
from scraping import scraping


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1')

@app.route("/", methods=["GET", "POST"])
def top():
    return render_template("top.html")

#新規登録

@app.route("/register", methods=["GET", "POST"])
def register():
    """
    GET: register.htmlの表示
    POST: ユーザの追加
    """
    if request.method == 'POST':
        # create user object
        new_user = User(
            username = request.form.get('username'),
            email = request.form.get("email"),
            password=generate_password_hash(request.form.get('password'), method='sha256')
        )
        print(new_user)
        db.session.add(new_user)
        db.session.commit()
        return redirect(redirect(url_for("main")))
    else:
        return render_template('register.html')
        # ------------------------------------------------------------------------

#ログイン機能

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET: loginページの表示
    POST: username, passwordの取得, sesion情報の登録
    """
    
    if request.method == 'POST':
        username =  request.form.get("username")
        email = request.form.get("email")
        password = request.form.get('password')
        # hash = generate_password_hash(password)
        # global status
        # Userテーブルからusernameに一致するユーザを取得
        user = User.query.filter_by(email=email, username=username).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect('/add')
    else:
        return render_template("login.html")

#ログアウト機能

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
    
# メイン画面

@app.route("/main", methods=["GET"])
def main():
    return render_template('main.html')

@app.route("/add", methods=["GET", "POST"])
def add():
    return render_template("add.html")

# スクレイピング機能

import codecs 
from scraping import scraping
from script import *
@app.route("/search", methods=["POST"])
def search():
    info=scraping(request.form.get("ISBN"))
    if info == None:
        script.al()
    if info != None:
        file = codecs.open("./templates/c.html",'w','utf-8','ignore')
        s = '\xa0'
        file.write(s)
        file.write("<meta charset='utf-8'>")
        file.write(info["title"])
        file.write(info["writer"])
        file.write(info["com"])
        # file.write('<a href="' + info["price"] + '">購入はこちら</a>\n')
        file.write('<img src="' + info["img_url"] + '">')
        file.close()
        return render_template('c.html')
