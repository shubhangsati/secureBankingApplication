# from app import db
from flask_cqlalchemy import CQLAlchemy
import uuid

db = CQLAlchemy()


class User(db.Model):
    uid = db.columns.UUID(default=uuid.uuid4)
    username = db.columns.Text(primary_key=True, required=True)
    password = db.columns.Text(required=True)
