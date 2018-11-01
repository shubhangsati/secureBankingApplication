# code to create table
# this is to create the database if you do not wish to do that manually using cqlsh
# you may use it to test database queries

from app import app
from models import db, User
from hashlib import sha256

db.init_app(app)  # initializes database

db.create_keyspace_simple('SBS', 1)  # creates keyspace if does not exist

db.sync_db()

# if there is not already a user with username admin
# create a user with username admin and password = sha256("admin")
if User.objects(username="admin").count() == 0:
    user1 = User.create(
        username="admin", password=str(
            sha256("admin").hexdigest()))
if User.objects(username="user").count() == 0:
    user1 = User.create(
        username="user", password=str(
            sha256("user").hexdigest()))
# if user already exists print user exists
else:
    print "User already exists"
