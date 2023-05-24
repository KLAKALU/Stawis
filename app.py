from flask import Flask
from flask import render_template, request, redirect, flash, url_for,session
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from scraping import scraping_
from flask_modals import Modal, render_template_modal
from dotenv import load_dotenv
from google.oauth2 import id_token
from google.auth.transport import requests as requsts_google
from requests_oauthlib import OAuth2Session
import requests
import os,datetime
from flask_oauthlib.client import OAuth
from getbookdetail import getbookdetail

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stawis.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
modal=Modal(app)
oauth = OAuth(app)

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login_manager.login_view = 'login'

# This allows us to use a plain HTTP callback
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

# 各APIのkeyを.envから取得
load_dotenv() 
rakuten_apikey = os.getenv('RAKUTEN_WEBAPI_KEY')
google_clientid = os.getenv('GOOGLE_APIKEY')
line_clientid = os.getenv('LINE_CLIENTID')
line_clientsecret = os.getenv('LINE_CLIENTSECRET')
line_authorization_base_url = 'https://access.line.me/oauth2/v2.1/authorize'
line_token_url = 'https://api.line.me/oauth2/v2.1/token'
line_redirect_uri = 'http://localhost:8080/line_login_callback'
line_verify_uri = 'https://api.line.me/oauth2/v2.1/verify'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    google_id = db.Column(db.Text)
    line_id = db.Column(db.Text)
    user_icon_path = db.Column(db.Text)
    reviews = db.relationship('Review', backref='user', lazy=True)

class Book(db.Model):
    isbn = db.Column(db.Integer, primary_key=True)
    image_pass = db.Column(db.String(100), unique=True)
    book_title = db.Column(db.String(100), unique=True)
    book_author = db.Column(db.String(100))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    isbn = db.Column(db.Integer)
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
        return render_template("register.html", google_clientid = google_clientid)

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
    
# googlelogin

@app.route('/googlelogin_callback', methods=['POST'])
def googlelogin_callback():
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        # idinfoは辞書型でデータを格納
        idinfo = id_token.verify_oauth2_token(request.form.get('credential'), requsts_google.Request(), google_clientid)

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        # そのgoogleアカウントのメールが既に登録済みの場合
        if User.query.filter_by(email=idinfo['email']).first():
            user = User.query.filter_by(email=idinfo['email']).first()
            login_user(user)
        # そのgoogleアカウントのメールがデータベースになく、新規登録の場合
        else:
            new_user = User(
            username = idinfo['name'],
            email = idinfo['email'],
            google_id = idinfo['sub']
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
    
#line-login

@app.route('/line_login', methods=['GET', 'POST'])
def line_login():
    line = OAuth2Session(line_clientid, redirect_uri=line_redirect_uri, scope='profile openid')
    authorization_url, state = line.authorization_url(line_authorization_base_url)
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route('/line_login_callback', methods=['GET'])
def line_login_callback():
    line = OAuth2Session(line_clientid, state=session['oauth_state'], redirect_uri=line_redirect_uri)
    token = line.fetch_token(line_token_url, client_secret=line_clientsecret,
                               authorization_response=request.url)
    session['oauth_token'] = token
    # line_data = OAuth2Session(line_clientid, token=session['oauth_token'])
    # idinfo = line_data.post('https://api.line.me/oauth2/v2.1/verify').json()
    # requestsを使い、データを取得
    payload = {'id_token': token["id_token"], 'client_id': line_clientid}
    r = requests.post(line_verify_uri,
        data=payload)
    json_data = r.json()
    print(json_data)
    print(token)
    new_user = User(
        username = json_data['name']
    )
    db.session.add(new_user)
    db.session.commit()
    # ここにフラッシュメッセージを追加
    login_user(new_user)
    session['logged_in']=True
    return redirect(url_for('main'))

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
    books = db.session.query(Book, Review).join(Book, Book.isbn == Review.isbn).filter(Review.user_id == current_user.id).all()
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
            try:
                book_data=getbookdetail(rakuten_apikey, isbn)
            except:
                flash('情報を取得することができませんでした。')
                return render_template("add.html")
            else:
                add_book = Book(
                isbn = isbn,
                # image_pass = book_data["img_url"],
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
    
#@app.route('/edit/<isbn>',methods=["POST"])
#def edit(isbn):
    #book = Book.query.get_or_404(isbn)
    #reviews = Review.query.filter_by(isbn=isbn).all()
    if request.method == 'POST':
        comment = request.form.get("comment")
        review = Review.query.filter_by(isbn=isbn).all()
        review.comment = comment
        db.session.commit()
        return redirect(url_for('main'))
    #return render_template('edit.html', reviews=reviews, book=book)
    
@app.route('/edit/<isbn>', methods=["POST"])
def edit(isbn):
    if request.method == 'POST':
        comment = request.form.get("comment")
        review = Review.query.filter_by(isbn=isbn).first()
        if review:
            review.comment = comment
        else:
            review = Review(isbn=isbn, comment=comment)
            db.session.add(review)
        db.session.commit()
        return redirect(url_for('main'))

#削除機能

@app.route('/delete/<isbn>')
def delete(isbn):
    book = Book.query.get_or_404(isbn)
    reviews = Review.query.filter_by(isbn=isbn).all()
    db.session.delete(book)
    for review in reviews:
        db.session.delete(review)
    db.session.commit()
    return redirect(url_for('main'))
