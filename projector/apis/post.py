from datetime import datetime
from flask import Blueprint, g, jsonify, request, Response
from projector import db
from projector.login_required import login_required
from projector.models import Post

bp = Blueprint("post", __name__, url_prefix="/post")


@bp.route("/list")
@login_required
def post_list():
    page = request.args.get("page", 1)
    per_page = request.args.get("perpage", 10)
    queried_posts = (
        Post.query.order_by(Post.creation_date.desc()).paginate(page, per_page).items
    )
    response = [post.serialize() for post in queried_posts]
    return jsonify(response)


@bp.route("/get/<int:postid>")
@login_required
def get(postid: int):
    post = Post.query.get(postid)
    return jsonify(post.serialize(fetch_content=True))


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
        authorid=g.user.userid,
    )
    db.session.add(post)  # type: ignore
    db.session.commit()  # type: ignore
    return ""


@bp.route("/edit/<int:postid>", methods=["PUT"])
@login_required
def edit(postid: int):
    post = Post.query.get(postid)
    if post.authorid != g.userid:
        return Response(status=403)
    json_data = request.get_json()
    title = json_data["title"]
    content = json_data["content"]
    post.title = title
    post.content = content
    db.session.commit()  # type: ignore
    return Response(status=200)
