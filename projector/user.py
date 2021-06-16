from flask_login import UserMixin
from projector import db
from projector.models import UserModel


class User(UserMixin):
    def __init__(self, userid, name, email):
        self.userid = userid
        self.name = name
        self.email = email

    @staticmethod
    def get(userid):
        user_from_db = UserModel.query.get(userid)
        if not user_from_db:
            return None
        user = User(user_from_db.userid, user_from_db.name, user_from_db.email)
        return user

    @staticmethod
    def create(userid, name, email):
        modeled_user = UserModel(userid=userid, name=name, email=email)
        db.session.add(modeled_user)
        db.session.commit()
