# type: ignore
from . import db


class UserModel(db.Model):
    userid = db.Column(db.Text(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)


class Project(db.Model):
    projectid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    adminid = db.Column(
        db.Integer, db.ForeignKey("user_model.userid", ondelete="CASCADE")
    )
    admin = db.relationship("UserModel", backref=db.backref("user_model_set"))
    members = db.Column(db.Text(), nullable=False)


class Post(db.Model):
    postid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text(), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    creation_date = db.Column(db.DateTime(), nullable=False)
    projectid = db.Column(
        db.Integer, db.ForeignKey("project.projectid", ondelete="CASCADE")
    )
    project = db.relationship("Project", backref=db.backref("post_set"))
    authorid = db.Column(
        db.Integer, db.ForeignKey("user_model.userid", ondelete="CASCADE")
    )
    author = db.relationship("UserModel", backref=db.backref("user_model_set"))
