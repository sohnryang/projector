from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile(os.path.join(os.path.dirname(__file__), "../config.py"))
    db.init_app(app)
    migrate.init_app(app, db)

    from .apis import auth, post, project

    app.register_blueprint(auth.bp)
    app.register_blueprint(post.bp)
    app.register_blueprint(project.bp)

    return app
