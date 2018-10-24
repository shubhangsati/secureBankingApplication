# code to create table

from app import db
from models import User
from hashlib import sha256

db.create_keyspace_simple('SBS', 1)

db.sync_db()

if User.objects(username="admin").count() == 0:
    user1 = User.create(
        username="admin", password=str(
            sha256("admin").hexdigest()))
else:
    print "User already exists"
