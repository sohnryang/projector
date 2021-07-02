from datetime import datetime
from flask import Blueprint, g, jsonify, request
from projector import db
from projector.login_required import login_required
from projector.models import Post, Project

bp = Blueprint("post", __name__, url_prefix="/post")


@bp.route("/list")
@login_required
def post_list():
    page = request.args.get("page", 1)
    per_page = request.args.get("perpage", 10)
    queried_posts = (
        Post.query.order_by(Post.creation_date.desc()).paginate(page, per_page).items
    )
    response = []
    for queried_post in queried_posts:
        post = {
            "postid": queried_post.postid,
            "title": queried_post.title,
            "author": queried_post.author,
            "project_name": queried_post.project.name,
            "creation_date": queried_post.creation_date.strftime("%y-%m-%d"),
        }
        response.append(post)
    return jsonify(response)


@bp.route("/content/<int:postid>")
@login_required
def post_content(postid: int):
    post = Post.query.get(postid)
    response = {
        "title": post.title,
        "author": post.author,
        "project_name": post.project.name,
        "creation_date": post.creation_date.strftime("%y-%m-%d"),
        "content": post.content,
    }
    return jsonify(response)


@bp.route("/create", methods=["POST"])
@login_required
def create():
    title = request.form["title"]
    content = request.form["content"]
    projectid = request.form["projectid"]
    post = Post(
        title=title,
        content=content,
        creation_date=datetime.now(),
        projectid=projectid,
        project=Project.query.get(projectid),
        author=g.user.name,
    )
    db.session.add(post)  # type: ignore
    db.session.commit()  # type: ignore
    return ""
