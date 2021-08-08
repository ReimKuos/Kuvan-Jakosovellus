from flask_sqlalchemy import SQLAlchemy
from os import getenv
from app import app

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///user"
db = SQLAlchemy(app)