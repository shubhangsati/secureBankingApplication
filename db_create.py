# code to create table
# this is to create the database if you do not wish to do that manually using cqlsh
# you may use it to test database queries

from app import app
from models import db, User
from hashlib import sha256
from functions import *

db.init_app(app)  # initializes database

db.create_keyspace_simple('SBS', 1)  # creates keyspace if does not exist

db.sync_db()

x0 = {
    "username": "user",
    "password": "user",
    "utype": "external-A",
    "firstname": "User",
    "lastname": "Sharma",
    "email": "user@mail.com",
    "AC": "11111",
    "balance": 1000,
    "branch": "Okhla",
    "address": "Delhi",
    "phone": "9911223344"
}
x1 = {
    "username": "admin",
    "password": "admin",
    "utype": "internal-C",
    "firstname": "Admin",
    "lastname": "Sati",
    "email": "admin@mail.com",
    "AC": "22222",
    "balance": 1000,
    "branch": "Okhla",
    "address": "Delhi",
    "phone": "9911223344"
}
x2 = {
    "username": "admin1",
    "password": "admin1",
    "utype": "internal-B",
    "firstname": "Admin1",
    "lastname": "Sati",
    "email": "admin1@mail.com",
    "AC": "22222",
    "balance": 1000,
    "branch": "Okhla",
    "address": "Delhi",
    "phone": "9911223344"
}
x3 = {
    "username": "admin2",
    "password": "admin2",
    "utype": "internal-A",
    "firstname": "Admin2",
    "lastname": "Sati",
    "email": "admin2@mail.com",
    "AC": "22222",
    "balance": 1000,
    "branch": "Okhla",
    "address": "Delhi",
    "phone": "9911223344"
}

x4 = {
    "username": "user1",
    "password": "user1",
    "utype": "external-A",
    "firstname": "User1",
    "lastname": "Paliwal",
    "email": "user1@mail.com",
    "AC": "22222",
    "balance": 5000,
    "branch": "Okhla",
    "address": "Delhi",
    "phone": "9911223344"
}

x5 = {
    "username": "user2",
    "password": "user2",
    "utype": "external-A",
    "firstname": "User2",
    "lastname": "Paliwal",
    "email": "user2@mail.com",
    "AC": "2222322",
    "balance": 5000,
    "branch": "Okhla",
    "address": "Delhi",
    "phone": "9911223344"
}
# if there is not already a user with username admin
# create a user with username admin and password = sha256("admin")
# createUser(x5)
if User.objects().count() == 0:
    createUser(x0)
    createUser(x1)
    createUser(x2)
    createUser(x3)
    createUser(x4)
# if user already exists print user exists
else:
    # u1 = User.objects(username='1')
    u1 = User.objects(username="admin").allow_filtering()
    u2 = User.objects(username="2").allow_filtering()
    temp = []
    for x in u1:
        temp.append(x)
    for x in u2:
        temp.append(x)
    print len(temp)
    # for x in [u1, u2]:
    #    print x[:]
    print "User already exists"
