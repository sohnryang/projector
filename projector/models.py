# type: ignore
from . import db


class UserModel(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    googleid = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def serialize(self):
        return {"user_id": self.userid, "name": self.name, "email": self.email}


class Project(db.Model):
    projectid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    adminid = db.Column(
        db.Integer, db.ForeignKey("user_model.userid", ondelete="CASCADE")
    )
    members = db.Column(db.Text(), nullable=False)

    def serialize(self):
        member_ids = self.members.split(",")
        members = []
        for member_id in member_ids:
            queried_user = UserModel.query.get(member_id)
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
        db.Integer, db.ForeignKey("user_model.userid", ondelete="CASCADE")
    )

    def serialize(self, fetch_content=False):
        author_name = UserModel.query.get(self.authorid).name
        project_name = Project.query.get(self.projectid).name
        serialized = {
            "post_id": self.postid,
            "title": self.title,
            "creation_date": self.creation_date.strftime("%Y-%m-%d"),
            "project_id": self.projectid,
            "project_name": project_name,
            "author_id": self.authorid,
            "author_name": author_name,
        }
        if fetch_content:
            serialized["content"] = self.content
        return serialized
