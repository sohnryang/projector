from flask import Blueprint, g, jsonify, request, Response
from projector.login_required import login_required
from projector import db
from projector.models import Project

bp = Blueprint("project", __name__, url_prefix="/project")


@bp.route("/create", methods=["POST"])
@login_required
def create():
    name = request.form["name"]
    description = request.form["description"]
    adminid = g.user.userid
    members = request.form["members"]
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
