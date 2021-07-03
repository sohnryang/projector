from flask import Blueprint, g, jsonify, request, Response
from projector.login_required import login_required
from projector import db
from projector.models import Project

bp = Blueprint("project", __name__, url_prefix="/project")


@bp.route("/create", methods=["POST"])
@login_required
def create():
    json_data = request.get_json()
    name = json_data["name"]
    description = json_data["description"]
    adminid = g.user.userid
    members = json_data["members"]
    project = Project(
        name=name,
        description=description,
        adminid=adminid,
        members=members,
    )
    db.session.add(project)  # type: ignore
    db.session.commit()  # type: ignore
    return Response(status=200)


@bp.route("/get/<int:projectid>")
@login_required
def get(projectid: int):
    project = Project.query.get(projectid)
    return jsonify(project.serialize())
