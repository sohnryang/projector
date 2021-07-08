from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request, Response
from google.oauth2 import id_token
from google.auth.transport import requests
from projector import db
from projector.models import UserModel

import jwt
import re

GOOGLE_CLIENT_ID = None
GOOGLE_CLIENT_SECRET = None
TOKEN_EXP_TIME = 60 * 60 * 24
JWT_SECRET_KEY = ""
email_pattern = re.compile(r".+@hana\.hs\.kr")

bp = Blueprint("auth", __name__, url_prefix="/auth")


def set_client(state):
    global GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, JWT_SECRET_KEY, TOKEN_EXP_TIME
    GOOGLE_CLIENT_ID = state.app.config["GOOGLE_CLIENT_ID"]
    GOOGLE_CLIENT_SECRET = state.app.config["GOOGLE_CLIENT_SECRET"]
    JWT_SECRET_KEY = state.app.config["JWT_SECRET_KEY"]
    TOKEN_EXP_TIME = state.app.config.get("TOKEN_EXP_TIME", 60 * 60 * 24)


bp.record(set_client)


@bp.route("/signin", methods=["POST"])
def signin():
    json_data = request.get_json()
    token = json_data["tokenId"]
    idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
    name = idinfo["name"]
    email = idinfo["email"]
    googleid = idinfo["sub"]
    if not re.fullmatch(email_pattern, email):
        return Response(status=403)
    user = UserModel.query.filter_by(googleid=str(googleid)).first()
    if not user:
        user = UserModel(name=name, email=email, googleid=str(googleid))
        db.session.add(user)  # type: ignore
        db.session.commit()  # type: ignore
    payload = {
        "userid": user.userid,
        "exp": datetime.utcnow() + timedelta(seconds=TOKEN_EXP_TIME),
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, "HS256")
    response = user.serialize()
    response["access_token"] = token
    return jsonify(response)
