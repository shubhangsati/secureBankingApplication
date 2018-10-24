from app import db
import uuid


class User(db.Model):
    uid = db.columns.UUID(default=uuid.uuid4)
    username = db.columns.Text(primary_key=True, required=True)
    password = db.columns.Text(required=True)
