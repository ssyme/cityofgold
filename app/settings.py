import os

SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(10)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "sqlite:///neochina.sqlite3"
UPLOAD_FOLDER = "static/media"
MAX_CONTENT_PATH = 500000
ALLOWED_EXTENSIONS = [".png", ".gif", ".jpeg", ".jpg"]
