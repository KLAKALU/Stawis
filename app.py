from flask import Flask
from flask import render_template, request, redirect, flash, url_for,session
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_sqlalchemy import SQLAlchemy
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

login_manager.login_view = 'login'

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
    book_author = db.Column(db.String(100))

class Review(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    isbn = db.Column(db.Integer)
    comment = db.Column(db.Text)
    date = db.Column(db.Integer)

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
        login_user(new_user)
        session['logged_in']=True
        return redirect(url_for('main'))
    else:
        print("error!")
        return render_template("register.html")

#ログイン機能

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET: loginページの表示
    POST: username, passwordの取得, sesion情報の登録
    """

    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get('password')
        # global status
        # Userテーブルからusernameに一致するユーザを取得
        user = User.query.filter_by(username=username).first()
        if check_password_hash(user.password, password):
            login_user(user)
            session['logged_in']=True
            return redirect(url_for('main'))
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
    session.pop('logged_in',None)
    return redirect("/")

# メイン画面

@app.route("/main", methods=["GET"])
@login_required
def main():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        book = db.session.query(Book).join(Review, Book.isbn == Review.isbn).filter(Review.user_id == current_user.id)
        print(book)
        return render_template('main.html',entries=book)

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
            comment = review
            # date = 
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
