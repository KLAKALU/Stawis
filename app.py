from flask import Flask
from flask import render_template, request, redirect, flash, url_for,session
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from scraping import scraping
from flask_modals import Modal, render_template_modal
from dotenv import load_dotenv
from google.oauth2 import id_token
from google.auth.transport import requests
import os,datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stawis.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
modal=Modal(app)

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login_manager.login_view = 'login'

# 各APIのkeyを.envから取得
load_dotenv() 
rakuten_apikey = os.getenv('RAKUTEN_WEBAPI_KEY')
google_clientid = os.getenv('GOOGLE_APIKEY')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    reviews = db.relationship('Review', backref='user', lazy=True)

class Book(db.Model):
    isbn = db.Column(db.Integer, primary_key=True)
    image_pass = db.Column(db.String(100), unique=True)
    book_title = db.Column(db.String(100), unique=True)
    book_author = db.Column(db.String(100))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    isbn = db.Column(db.Integer, db.ForeignKey('book.isbn'))
    comment = db.Column(db.Text)
    date = db.Column(db.Text)

if __name__ == '__main__':
    app.debug = True
    # app.run(host='127.0.0.1')
    app.run()

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
        username = request.form.get('username')
        email = request.form.get("email")
        # ユーザ名が既にある場合
        if User.query.filter_by(username=username).first():
            flash('そのユーザー名は既に使われています')
            return render_template("register.html", google_clientid = google_clientid)
        if User.query.filter_by(email=email).first():
            flash('そのメールアドレスは既に登録されています')
            return render_template("register.html", google_clientid = google_clientid)
        new_user = User(
            username = username,
            email = email,
            password=generate_password_hash(request.form.get('password'), method='sha256')
        )
        print(new_user)
        db.session.add(new_user)
        db.session.commit()
        # ここにフラッシュメッセージを追加
        login_user(new_user)
        session['logged_in']=True
        return redirect(url_for('main'))
    else:
        print("error!")
        return render_template("register.html, google_clientid = google_clientid")

#ログイン機能

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET: loginページの表示
    POST: username, passwordの取得, session情報の登録
    """

    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get('password')
        # global status
        # Userテーブルからusernameに一致するユーザを取得
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                session['logged_in']=True
                return redirect(url_for('main'))
        #userが取得できない、又はパスワードが違う場合
        flash('ユーザー名かパスワードが間違っています')
        return render_template("login.html", username = username)
    else:
        return render_template("login.html", google_clientid = google_clientid)

@app.route('/googlelogin_callback', methods=['POST'])
def googlelogin_callback():
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        # idinfoは辞書型でデータを格納
        idinfo = id_token.verify_oauth2_token(request.form.get('credential'), requests.Request(), google_clientid)

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        # そのgoogleアカウントのメールが既に登録済みの場合
        print(idinfo)
        if User.query.filter_by(email=idinfo['email']).first():
            user = User.query.filter_by(email=idinfo['email']).first()
            login_user(user)
        # そのgoogleアカウントのメールがデータベースになく、新規登録の場合
        else:
            new_user = User(
            username = idinfo['name'],
            email = idinfo['email'],
            )
            db.session.add(new_user)
            db.session.commit()
            # ここにフラッシュメッセージを追加
            login_user(new_user)
        session['logged_in']=True
        return redirect(url_for('main'))
    except ValueError:
        # Invalid token
        print('error! Invalid token')
        flash('googleアカウントでの認証に失敗しました')
        return redirect(url_for('login'))

#ログアウト機能

@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop('logged_in',None)
    return redirect("/")

# メイン画面

@app.route("/main", methods=["GET"])
@login_required
def main():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        books = db.session.query(Book, Review).join(Book, Book.isbn == Review.isbn).filter(Review.user_id == current_user.id).all()
        print(books)
        return render_template_modal('main.html',books=books)

#add画面

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == 'POST':
        isbn = request.form.get("ISBN")
        review = request.form.get("review")

        # Bookテーブルに本情報がなかった場合
        if not Book.query.filter_by(isbn=isbn).first():
            book_data=scraping(isbn)
            if book_data == None:
                flash('情報を取得することができませんでした。')
                return render_template("add.html")
            else:
                add_book = Book(
                isbn = isbn,
                image_pass = book_data["img_url"],
                book_title = book_data["title"],
                book_author = book_data["writer"]
                )
                db.session.add(add_book)

        add_reviews=Review(
            user_id = current_user.id,
            isbn = isbn,
            comment = review,
            date = datetime.datetime.now().strftime('%Y-%m-%d')
        )
        db.session.add(add_reviews)
        db.session.commit()
        flash("本が追加されました")
        return redirect(url_for('main'))
    elif request.method == 'GET':
        return render_template("add.html")

# ポップアップ画面用のエンドポイント

@app.route('/popup/<data>')
def popup(data):
    # 画面から送られてきたデータを表示するため、データも一緒に送信
    return render_template('popup.html', data=data)

#レビュー
@app.route('/review/<isbn>')
def review(isbn):
    book = Book.query.get_or_404(isbn)
    reviews = Review.query.filter_by(isbn=isbn).all()
    return render_template("review.html", book=book, reviews=reviews)

#編集機能
    
@app.route('/edit/<isbn>',methods=["GET", "POST"])
def edit(isbn):
    book = Book.query.get_or_404(isbn)
    reviews = Review.query.filter_by(isbn=isbn).all()
    if request.method == 'POST':
        comment = request.form.get("comment")
        review = Review.query.filter_by(isbn=isbn).first()
        review.comment = comment
        db.session.commit()
        return redirect(url_for('main'))
    return render_template('edit.html', reviews=reviews, book=book)