from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app =   Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class books(db.Model):
    isbn = db.Column(db.Integer, primary_key=True)
    image_pass = db.Column(db.text, unique=True)
    book_title = db.Column(db.text, unique=True)
    bool_author = db.Column(db.text)

@app.route('/')
def index():
    return render_template

# 本を登録するデータベースを作る