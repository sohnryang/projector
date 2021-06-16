import os

BASE_DIR = os.path.dirname(__file__)
SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "projector.db")}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(30).hex())
