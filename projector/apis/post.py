from bs4 import BeautifulSoup, Tag
from collections import deque
from datetime import datetime
from flask import Blueprint, g, jsonify, request, Response
from projector import db
from projector.login_required import login_required
from projector.models import Post
from typing import List

import requests

bp = Blueprint("post", __name__, url_prefix="/post")
HANA_INTRANET_BOARD_URL = (
    "https://hi.hana.hs.kr/SYSTEM_Community/Board/Student_Board/student.asp"
)


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


def html_to_markdown(elements: List[Tag]):
    result = []
    for element in elements:
        stack = deque([*reversed(list(element.children))])
        while stack:
            node = stack.pop()
            if node.name is None:
                text = str(node)
                if text.isspace():
                    continue
                result.append(str(node))
            elif node.name == "img":
                if "name" in node.attrs and "wiz_" in node["name"]:
                    continue
                result.append(
                    f"Images are not yet supported... URL: {node['src']}"
                )  # TODO: support images
            elif node.name == "a":
                result.append(f"[{node.text.strip()}]({node['href']})")
            else:
                for child in reversed(list(node.children)):
                    stack.append(child)
    return "\n\n".join(result)


@bp.route("/import/<int:bbs_idx>", methods=["POST"])
@login_required
def import_post(bbs_idx: int):
    json_data = request.get_json()
    hana_username = json_data["hana_username"]
    hana_password = json_data["hana_password"]
    project_id = json_data["project_id"]
    with requests.Session() as sess:
        sess.post(
            "https://hi.hana.hs.kr/proc/login_proc.asp",
            data={
                "login_id": hana_username,
                "login_pw": hana_password,
                "x": "0",
                "y": "0",
            },
        )
        res_edit = sess.get(f"{HANA_INTRANET_BOARD_URL}?mode=update&bbs_idx={bbs_idx}")
        if res_edit.status_code == 302:
            return Response(status=403)
        res = sess.get(f"{HANA_INTRANET_BOARD_URL}?mode=view&bbs_idx={bbs_idx}")
        soup = BeautifulSoup(res.content, "html.parser")
        title = soup.select_one(".subject").text
        contents = soup.find("div", {"class": "content"}).find_all(["p", "img"])
        markdown = html_to_markdown(contents)
    post = Post(
        title=title,
        content=markdown,
        creation_date=datetime.now(),
        projectid=project_id,
        authorid=g.user.userid,
    )
    db.session.add(post)  # type: ignore
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
