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
        db.Text(), db.ForeignKey("user_model.userid", ondelete="CASCADE")
    )
    members = db.Column(db.Text(), nullable=False)

    def serialize(self):
        member_emails = self.members.split(",")
        members = []
        for email in member_emails:
            queried_user = UserModel.query.filter(UserModel.email == email).first()
            if not queried_user:
                continue
            members.append(queried_user.name)
        return {
            "project_id": self.projectid,
            "name": self.name,
            "admin_name": UserModel.query.get(self.adminid).name,
            "member_names": members,
            "description": self.description,
        }


class Post(db.Model):
    postid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text(), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    creation_date = db.Column(db.DateTime(), nullable=False)
    projectid = db.Column(
        db.Integer, db.ForeignKey("project.projectid", ondelete="CASCADE")
    )
    authorid = db.Column(
        db.Text(), db.ForeignKey("user_model.userid", ondelete="CASCADE")
    )
