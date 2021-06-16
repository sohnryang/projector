from . import db


class UserModel(db.Model):
    userid = db.Column(db.Text(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
