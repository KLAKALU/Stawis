from flask import Flask, request, render_template

app = Flask(__name__)



@app.route("/", methods=["GET", "POST"])
def register():
    #if request.method == 'POST':
      #email = request.form.get("email")
      #password = request.form.get('password')
      #confirmation = request.form.get('confirm_password')
      #username = request.form.get('username')
      #if password != confirmation:
       # error_message = "確認用パスワードと一致しませんでした。"
        # エラーメッセージ付きでregister.htmlに渡す
        #return render_template("register.html", error_message=error_message)
    return render_template("register.html")


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1')
