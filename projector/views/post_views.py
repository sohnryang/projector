from flask import Blueprint, render_template
from flask_login import login_required
from projector.models import Post

bp = Blueprint("post", __name__, url_prefix="/post")


@bp.route("/<int:postid>")
@login_required
def post_detail(postid: int):
    post = Post.query.get_or_404(postid)
    return render_template("post.html", post=post)
