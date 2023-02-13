from flask import request, redirect, url_for, render_template, flash, session
from stawis2 import app
from stawis2  import db
from stawis2.models.users import User
from stawis2.views.loging import login_required
from flask import Blueprint


user = Blueprint('user', __name__)

@user.route('/users', methods=['POST'])
def add_user():
        user = User(
            username=request.form['username'],
            password=request.form['password']
            )
        db.session.add(user)
        db.session.commit()
        flash('新規ユーザ登録が完了しました。ログインしてください。')
        return redirect(url_for('loging.login'))



@user.route('/users/new', methods=['GET'])
def new_user():
    return render_template('users/register.html', id='user')
