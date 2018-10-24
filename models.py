# from app import db
from flask_cqlalchemy import CQLAlchemy
import uuid

db = CQLAlchemy()  # create a CQLAlchemy wrapper [uses cassandra-driver]

# Database model for User
# represents a table in the database


class User(db.Model):
    # Todo: set user id as the primary key
    # user id
    uid = db.columns.UUID(default=uuid.uuid4)
    # Todo: username should be unique, required
    username = db.columns.Text(primary_key=True, required=True)
    # password, required
    password = db.columns.Text(required=True)
