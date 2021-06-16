from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile(os.path.join(os.path.dirname(__file__), "../config.py"))
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    from . import models

    from .views import login_views, main_views, dashboard_views

    app.register_blueprint(login_views.bp)
    app.register_blueprint(main_views.bp)
    app.register_blueprint(dashboard_views.bp)

    return app
