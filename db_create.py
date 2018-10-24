# code to create table

from app import app
from models import db, User
from hashlib import sha256

db.init_app(app)

db.create_keyspace_simple('SBS', 1)

db.sync_db()

if User.objects(username="admin").count() == 0:
    user1 = User.create(
        username="admin", password=str(
            sha256("admin").hexdigest()))
else:
    print "User already exists"
