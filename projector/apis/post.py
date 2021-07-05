from datetime import datetime
from flask import Blueprint, g, jsonify, request, Response
from projector import db
from projector.login_required import login_required
from projector.models import Post

bp = Blueprint("post", __name__, url_prefix="/post")


@bp.route("/list")
@login_required
def post_list():
    queried_posts = Post.query.order_by(Post.creation_date.desc())
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
    json_data = request.get_json()
    title = json_data["title"]
    content = json_data["content"]
    projectid = int(json_data["projectid"])
    post = Post(
        title=title,
        content=content,
        creation_date=datetime.now(),
        projectid=projectid,
        authorid=g.user.userid,
    )
    db.session.add(post)  # type: ignore
    db.session.commit()  # type: ignore
    return Response(status=200)


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


@bp.route("/filter-by-project/<int:projectid>", methods=["POST"])
@login_required
def search(projectid: int):
    queried_posts = Post.query.filter_by(projectid=projectid)
    return jsonify([post.serialize() for post in queried_posts])


@bp.route("/filter-by-projects", methods=["POST"])
@login_required
def search_multiple():
    json_data = request.get_json()
    projects = json_data["projects"]
    queried_posts = Post.query.filter(Post.projectid.in_(projects))
    return jsonify([post.serialize() for post in queried_posts])
