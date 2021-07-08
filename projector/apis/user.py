from flask import Blueprint, jsonify, Response
from projector.login_required import login_required
from projector.models import UserModel

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/get/<int:userid>", methods=["GET"])
@login_required
def get(userid: int):
    user = UserModel.query.get(userid)
    if user is None:
        return Response(status=404)
    return jsonify(user.serialize())


@bp.route("/search-by-email/<email>", methods=["POST"])
@login_required
def search_by_email(email: str):
    user = UserModel.query.filter_by(email=email).first()
    if user is None:
        return Response(status=404)
    return jsonify(user.serialize())
