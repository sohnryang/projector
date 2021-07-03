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


@bp.route("/edit/<int:projectid>", methods=["PUT"])
@login_required
def edit(projectid: int):
    project = Project.query.get(projectid)
    if project.adminid != g.userid:
        return Response(status=403)
    json_data = request.get_json()
    name = json_data["name"]
    description = json_data["description"]
    members = json_data["members"]
    project.name = name
    project.description = description
    project.members = members
    db.session.commit()  # type: ignore
    return Response(status=200)


@bp.route("/search/<keyword>", methods=["POST"])
@login_required
def search(keyword: str):
    queried_projects = Project.query.filter(Project.name.ilike(f"%{keyword}%"))
    return jsonify([project.serialize() for project in queried_projects])


@bp.route("/get/<int:projectid>")
@login_required
def get(projectid: int):
    project = Project.query.get(projectid)
    return jsonify(project.serialize())
