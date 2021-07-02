from datetime import datetime, timedelta
from flask import Blueprint, current_app, jsonify, url_for, redirect, request
from oauthlib.oauth2 import WebApplicationClient
from projector import db
from projector.models import UserModel

import json
import jwt
import re
import requests

GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
GOOGLE_CLIENT_ID = None
GOOGLE_CLIENT_SECRET = None
TOKEN_EXP_TIME = None
JWT_SECRET_KEY = None
client = WebApplicationClient(GOOGLE_CLIENT_ID)
email_pattern = re.compile(r".+@hana\.hs\.kr")

bp = Blueprint("auth", __name__, url_prefix="/auth")
provider_config = lambda: requests.get(GOOGLE_DISCOVERY_URL).json()


def set_client(state):
    global GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, JWT_SECRET_KEY, TOKEN_EXP_TIME, client
    GOOGLE_CLIENT_ID = state.app.config["GOOGLE_CLIENT_ID"]
    client = WebApplicationClient(GOOGLE_CLIENT_ID)
    GOOGLE_CLIENT_SECRET = state.app.config["GOOGLE_CLIENT_SECRET"]
    JWT_SECRET_KEY = state.app.config["JWT_SECRET_KEY"]
    TOKEN_EXP_TIME = state.app.config.get("TOKEN_EXP_TIME", 60 * 60 * 24)


bp.record(set_client)


@bp.route("/signin")
def signin():
    auth_endpoint = provider_config()["authorization_endpoint"]
    req_uri = client.prepare_request_uri(
        auth_endpoint,
        redirect_uri=url_for("auth.callback", _external=True),
        scope=["openid", "email", "profile"],
    )
    return redirect(req_uri)


@bp.route("/callback")
def callback():
    code = request.args.get("code")
    token_endpoint = provider_config()["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    client.parse_request_body_response(json.dumps(response.json()))
    userinfo_endpoint = provider_config()["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        user_email = userinfo_response.json()["email"]
        user_name = userinfo_response.json()["name"]
    else:
        return "User email not available", 400
    if not re.fullmatch(email_pattern, user_email):
        return "하나고등학교 계정만 가능합니다. <a href='/auth/signin'>돌아가기</a>", 403
    user = UserModel(userid=unique_id, name=user_name, email=user_email)
    if not UserModel.query.get(str(unique_id)):
        db.session.add(user)  # type: ignore
        db.session.commit()  # type: ignore
    payload = {
        "userid": unique_id,
        "exp": datetime.utcnow()
        + timedelta(seconds=current_app.config.get("TOKEN_EXP_TIME", 60 * 60 * 24)),
    }
    token = jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], "HS256")
    return jsonify({"access_token": token})
