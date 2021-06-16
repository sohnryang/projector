from flask import Flask

import os

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile(os.path.join(os.path.dirname(__file__),
                                        '../config.py'))

    from .views import login_views, main_views
    app.register_blueprint(login_views.bp)
    app.register_blueprint(main_views.bp)

    return app
