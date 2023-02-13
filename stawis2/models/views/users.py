@user.route('/users/new', methods=['GET'])
# 新規投稿フォーム
def new_user():
    return render_template('users/new.html', id='user')


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
    return render_template('users/new.html', id='user')
