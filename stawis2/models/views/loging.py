from flask import request, redirect, url_for, render_template, flash, session
from cafe_site import app
from functools import wraps
from cafe_site.models.users import User
import bcrypt
from flask import Blueprint

loging = Blueprint('loging', __name__)

def login_required(loging):
    @wraps(loging)
    def inner(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('loging.login'))
        return loging(*args, **kwargs)
    return inner


@loging.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
            user = User.query.filter_by(username=request.form['username']).first()
        except:
            flash('ユーザ名が異なります')
            return render_template('login.html')
        if request.form['username'] != user.username:
            flash('ユーザ名が異なります')
        elif bcrypt.hashpw(request.form['password'].encode(), user.salt.encode()).decode() != user.password:
            flash('パスワードが異なります')
        else:
            session['logged_in'] = True
            session['user_id'] = user.id
            flash('ログインしました')
            return redirect(url_for('review.show_reviews'))
    return render_template('login.html', id="login")

@loging.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('ログアウトしました')
    return redirect(url_for('review.show_reviews'))

@loging.app_errorhandler(404)
def non_existant_route(error):
    return redirect(url_for('loging.login'))