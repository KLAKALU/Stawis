from flask import Flask
from flask import render_template, request, redirect
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stawis.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

# ログインページのエンドポイント
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))


login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/add", methods=["GET", "POST"])
def add():
    return render_template("add.html")

@app.route("/", methods=["GET", "POST"])
def top():
    return render_template("top.html")



if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1')


#ログアウト機能

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

#新規登録
@app.route("/register", methods=["GET", "POST"])
def register():
    """
    GET: register.htmlの表示
    POST: ユーザの追加
    """
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get('password')
        confirmation = request.form.get('repassword')
        username = request.form.get('username')
        #
        user = User(email=email,username=username, password=generate_password_hash(password, method='sha256'))
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('register.html')

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

        # Userテーブルからusernameに一致するユーザを取得
        user = User.query.filter_by(email=email, username=username).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
    else:
        return render_template("login.html")
