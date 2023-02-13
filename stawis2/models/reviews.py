from stawis2 import db
from datetime import datetime

class Review(db.Model):
    from stawis2.models.users import User
    __tablename__ = 'Reviews'
    id = db.Column(db.Integer, primary_key=True)
    star = db.Column(db.Integer)
    title = db.Column(db.String(50), unique=True)
    text = db.Column(db.Text)
# usersテーブルのidを外部キーとして取得
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
# Reviewsテーブルのuserカラムにusersテーブルのuser_idカラムを関連付ける
    user = db.relationship('User', foreign_keys=user_id)
    created_at = db.Column(db.DateTime)

    def __init__(self, star=None, title=None, text=None, user_id=None):
        self.star = star
        self.title = title
        self.text = text
        self.user_id = user_id
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<Review id:{} star:{} title:{} text:{} user_id:{}>'.format(self.id, self.star, self.title, self.text, self.user_id)