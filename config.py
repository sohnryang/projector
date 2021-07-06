import os

BASE_DIR = os.path.dirname(__file__)
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL", "postgresql://curling_grad@localhost:5432/projector"
)
SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres:", "postgresql:")
SQLALCHEMY_TRACK_MODIFICATIONS = False
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", os.urandom(30).hex())
SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(30).hex())
