from flask import current_app, g, request, Response
from functools import wraps
from projector.models import UserModel

import jwt


def login_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        access_token = request.headers.get("Authorization")
        if access_token is not None:
            try:
                payload = jwt.decode(
                    access_token,
                    current_app.config["JWT_SECRET_KEY"],
                    algorithms="HS256",
                )
            except jwt.InvalidTokenError:
                payload = None
            userid = payload["userid"]
            g.userid = userid
            g.user = UserModel.query.get(str(userid))
        else:
            return Response(status=401)
        return f(*args, **kwargs)

    return decorated_func
