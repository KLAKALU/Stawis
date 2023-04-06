from flask import Flask
from flask import render_template, request, redirect, flash, url_for
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_sqlalchemy import SQLAlchemy
import codecs
from scraping import scraping


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stawis.db'
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
    reviews = db.relationship('Review', backref='user', lazy=True)

class Book(UserMixin,db.Model):
    isbn = db.Column(db.Integer, primary_key=True)
    image_pass = db.Column(db.String(100), unique=True)
    book_title = db.Column(db.String(100), unique=True)
    bool_author = db.Column(db.String(100))

class Review(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    isbn = db.column(db.Integer)
    comment = db.column(db.Text)
    date = db.column(db.Integer)

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
        # return 'User created successfully'
        # ここにフラッシュメッセージを追加
        return render_template('main.html')
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
        password = request.form.get('password')
        # global status
        # Userテーブルからusernameに一致するユーザを取得
        user = User.query.filter_by(username=username).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect('/main')
        else:
            print("error!")
            return render_template("login.html")
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
    books_entries = Book.query.all()
    review_entries=Review.query.all()
    main_entry = []
    for book_entry in books_entries:
        username = User.query.filter_by(id=book_entry.user_id).first().username
        main_entry.append({'username': username, 'book': book_entry.book_title})
    return render_template('main.html',entries=main_entry)

#add画面

import codecs
from scraping import scraping
@app.route("/add", methods=["GET", "POST"])
def add():
    add_entry=User.query.all()
    if request.method == 'POST':
        info=scraping(request.form.get("ISBN"))
        if info == None:
            flash('存在しないISBNが入力されました')
            return render_template("add.html")
        if info != None:
            print("foo")
        file=open("isbn.txt")
        search_isbn=file.read()
        info=scraping(search_isbn)
        add_book=Book(
        isbn=search_isbn,
        image_pass=info["img_url"],
        book_title=info["title"],
        bool_author=info["writer"]
        )
        db.session.add(add_book)
        db.session.commit()
        flash("本が追加されました")
        return render_template("main.html")
    if request.method == 'GET':
        return render_template("add.html",entries=add_entry)

# スクレイピング機能

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == 'POST':
        info=scraping(request.form.get("ISBN"))
        if info == None:
            flash('存在しないISBNが入力されました')
            return render_template("add.html")
        if info != None:
            txt_file=codecs.open("isbn.txt","w")
            txt_file.write(request.form.get("ISBN"))
            txt_file.close()
            file = codecs.open("./templates/c.html",'w','utf-8','ignore')
            s = '\xa0'
            file.write(s)
            file.write("<meta charset='utf-8'>")
            file.write(info["title"])
            file.write(info["writer"])
            #file.write(info["com"])
            file.write('<img src="' + info["img_url"] + '">')
            file.close()
            return render_template('c.html')

# ポップアップ画面用のエンドポイント

@app.route('/popup/<data>')
def popup(data):
    # 画面から送られてきたデータを表示するため、データも一緒に送信
    return render_template('popup.html', data=data)
