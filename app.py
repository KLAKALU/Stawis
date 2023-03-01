from flask import Flask
from flask import render_template, request, redirect
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), nullable=False, unique=True)
	password = db.Column(db.String(25))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app = Flask(__name__)


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
    return redirect("/")

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

        user = User(email=email,username=username,confirmation=confirmation, password=generate_password_hash(password, method='sha256'))
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
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
            return redirect('/')
    else:
        return render_template("login.html")

#ISBN検索
def scraping(isbn):
    url=r"https://www.kinokuniya.co.jp/f/dsg-01-" + str(isbn)
    open_=requests.get(url)
    soup_=bs4.BeautifulSoup(open_.content,"html.parser")
    title=soup_.select('h3[itemprop="name"]')
    writer=soup_.select('div[class="infobox ml10 mt10"] > ul > li')
    com=soup_.select('div[class="infobox ml10 mt10"] > ul > li > a')
    price=soup_.select('div[class="infobox ml10 mt10"] > ul > li')
    soup_img = bs4.BeautifulSoup(requests.get(url).content, 'lxml')
    src=[]
    for link in soup_img.find_all('img'):
        if link.get('src').endswith('.jpg'):
            src.append(link.get('src'))
    if src==[]:
        print("表紙画像が見つかりませんでした")
    else:
        img_src=src[1]
        img_url="https://www.kinokuniya.co.jp" + img_src[2:]
        res = requests.get(img_url, stream=True)
        if res.status_code == 200:
            img=open("./static/img/im.jpg", 'wb')
            res.raw.decode_content = True
            shutil.copyfileobj(res.raw, img)
    if title==[] and writer==[] and com==[] and price==[]:
        return "本が見つかりませんでした。"
    else:
        title_=title[0].getText()
        writer_=writer[0].getText()
        com_=com[1].getText()
        price_=price[2].getText()
        info=[title_, writer_, com_, price_, url]
    ***REMOVED***

import requests,bs4,codecs
@app.route("/search", methods=["POST"])
def search():
    if request.method == "POST":
        scraping(request.form['ISBN'])
        file = codecs.open("./templates/c.html",'w','utf-8','ignore')
        s = '\xa0'
        file.write(s)
        file.write("<meta charset='utf-8'>")
        file.write(scraping(request.form['ISBN'][0:3]))
        file.write('<a href="' + scraping(request.form['ISBN'])[4] + '">購入はこちら</a>\n')
        file.write('<img src="' + './static/im.jpg' + '">')
        file.close()
        return render_template('c.html')