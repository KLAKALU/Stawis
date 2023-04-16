from flask import Flask
from flask import render_template,request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stawis.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/delete', methods=['POST'])
@login_required
def delete_connect():
    id = request.form['impressions']
    user = delete_connect.query.get(id)

    with  db.session.begin(subtransactions=True):
        db.session.delet(user)
        db.session.commit()
    return redirect(url_for('top'))