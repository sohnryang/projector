from flask import Blueprint, render_template
from flask_login import login_required
from projector.models import Post

bp = Blueprint("list", __name__, url_prefix="/list")


@bp.route("/")
@login_required
def index():
    post_list = Post.query.order_by(Post.creation_date.desc())
    return render_template("dashboard.html", post_list=post_list)
