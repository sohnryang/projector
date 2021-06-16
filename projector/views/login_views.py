from flask import Blueprint, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from oauthlib.oauth2 import WebApplicationClient
from werkzeug.utils import redirect
from projector import login_manager
from projector.user import User

import json
import re
import requests

GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

bp = Blueprint("login", __name__, url_prefix="/login")
GOOGLE_CLIENT_ID = ""
GOOGLE_CLIENT_SECRET = ""
client = None
email_pattern = re.compile(r".+@hana\.hs\.kr")


@login_manager.user_loader
def load_user(userid):
    return User.get(userid)


def get_google_provider_config():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


def set_client(state):
    global GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, client
    GOOGLE_CLIENT_ID = state.app.config["GOOGLE_CLIENT_ID"]
    client = WebApplicationClient(GOOGLE_CLIENT_ID)
    GOOGLE_CLIENT_SECRET = state.app.config["GOOGLE_CLIENT_SECRET"]


bp.record(set_client)


@bp.route("/")
def login():
    if current_user.is_authenticated:
        return (
            f"<pre>id: {current_user.userid}\n"
            f"name: {current_user.name}\n"
            f"email: {current_user.email}</pre><br />\n"
            "<a href='/login/logout'>Log out</a>"
        )
    else:
        return render_template("login.html")


@bp.route("/googlelogin")
def googlelogin():
    config = get_google_provider_config()
    endpoint = config["authorization_endpoint"]
    req_uri = client.prepare_request_uri(
        endpoint,
        redirect_uri=url_for("login.callback", _external=True),
        scope=["openid", "email", "profile"],
    )
    return redirect(req_uri)


@bp.route("/callback")
def callback():
    code = request.args.get("code")
    config = get_google_provider_config()
    token_endpoint = config["token_endpoint"]
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
    userinfo_endpoint = config["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        user_email = userinfo_response.json()["email"]
        user_name = userinfo_response.json()["name"]
    else:
        return "User email not available", 400
    if not re.fullmatch(email_pattern, user_email):
        return "Must be HAS Account. <a href='/login'>Go back</a>", 403
    user = User(userid=unique_id, name=user_name, email=user_email)
    if not User.get(unique_id):
        User.create(unique_id, user_name, user_email)
    login_user(user)
    return redirect(url_for("main.index"))


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))
