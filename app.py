from flask import Flask, request, render_template,  flash, session, datetime, redirect, psycopg2_connect, check_password_hash, generate_password_hash


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
def logout():
    # セッション情報をクリア
    session.clear()
    # グローバル変数をlogout状態に
    global status
    status = False
    flash("ログアウトが完了しました。")
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

        error_message = ""

        if password != confirmation:
            error_message = "確認用パスワードと一致しませんでした。"
            # エラーメッセージ付きでregister.htmlに渡す
            return render_template("register.html", error_message=error_message)
        # --------------------------------------------------------------------------------
        conn = psycopg2_connect()    #データベース名
        dt = datetime.datetime.now()
        with conn:
            with conn.cursor() as cur:
                
                cur.execute('SELECT * FROM users;')
                # print(cur.fetchall())
                email_data = cur.fetchall()

                for row in email_data:
                    print(row)
                    if row[1] == email:
                        error_message = "そのemailアドレスは登録済みです"
                        # エラーメッセージ付きでregister.htmlに渡す
                        return render_template("register.html", error_message=error_message)

                cur.execute("INSERT INTO users(email, password, name, registered_at) VALUES(%s, %s, %s, %s);", (email, generate_password_hash(password), username, dt))
            conn.commit
        # ------------------------------------------------------------------------

        # 新規登録後はlogin画面へ
        return redirect ("/login")

    else:
        return render_template("register.html")

#ログイン機能

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET: loginページの表示
    POST: username, passwordの取得, sesion情報の登録
    """
    global status
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get('password')
        # hash = generate_password_hash(password)
        # global status

        error_message = ""

        # PostgreSQL Server へ接続
        con = psycopg2_connect()
        cur = con.cursor()
        cur.execute("SELECT password, id FROM users WHERE email = %s", (email,))
        user_data = cur.fetchall()
        # メールアドレス：ユーザーデータは1:1でないといけない（新規登録画面でその処理書いてくれると嬉しいです！（既に同じメールアドレスが存在している場合はエラーメッセージを渡す等））
        if len(user_data) == 1:
            for row in user_data:
                if check_password_hash(row[0], password):
                    con.close()
                    session["id"] = row[1]
                    status = True
                    return redirect("/")                   
                    # return render_template("index2.html", status=status)
                else:
                    con.close()
                    error_message = "パスワードが異なります"
                    return render_template("login.html", error_message=error_message)
        else:
            con.close()
            # ↓現段階では登録されていない or メールアドレスが重複して登録されている
            error_message = "入力されたメールアドレスは登録されていません"
            return render_template("login.html", error_message=error_message)
    else:
        return render_template("login.html")


