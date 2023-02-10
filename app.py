from flask import Flask, request, render_template

app = Flask(__name__)



@app.route("register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return "Success"
    else:
        return render_template("register.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")
@app.route("/add", methods=["GET", "POST"])
def add():
    return render_template("add.html")
@app.route("/", methods=["GET", "POST"])
def top():
    return render_template("top.html")

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1')
