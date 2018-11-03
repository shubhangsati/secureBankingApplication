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

x1 = {
    "username": "admin",
    "password": "admin",
    "utype": "internal-C",
    "firstname": "Admin",
    "lastname": "Sati",
    "email": "admin@mail.com",
    "AC": "-----",
    "balance": 1000,
    "branch": "Okhla",
    "address": "Delhi",
    "phone": "9999999999"
}
x2 = {
    "username": "admin1",
    "password": "admin1",
    "utype": "internal-B",
    "firstname": "Admin1",
    "lastname": "Sati",
    "email": "admin1@mail.com",
    "AC": "-----",
    "balance": 1000,
    "branch": "Okhla",
    "address": "Delhi",
    "phone": "8888888888"
}
x3 = {
    "username": "admin2",
    "password": "admin2",
    "utype": "internal-A",
    "firstname": "Admin2",
    "lastname": "Sati",
    "email": "admin2@mail.com",
    "AC": "-----",
    "balance": 1000,
    "branch": "Okhla",
    "address": "Delhi",
    "phone": "7777777777"
}

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
    "phone": "0000000000"
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
    "phone": "9999999999"
}

x5 = {
    "username": "user2",
    "password": "user2",
    "utype": "external-A",
    "firstname": "User2",
    "lastname": "Paliwal",
    "email": "user2@mail.com",
    "AC": "33333",
    "balance": 5000,
    "branch": "Okhla",
    "address": "Delhi",
    "phone": "8888888888"
}

x6 = {
    "username": "user3",
    "password": "user3",
    "utype": "external-A",
    "firstname": "user3",
    "lastname": "Paliwal",
    "email": "user3@mail.com",
    "AC": "44444",
    "balance": 5000,
    "branch": "Okhla",
    "address": "Delhi",
    "phone": "7777777777"
}

x7 = {
    "username": "user4",
    "password": "user4",
    "utype": "external-A",
    "firstname": "user4",
    "lastname": "Paliwal",
    "email": "user4@mail.com",
    "AC": "55555",
    "balance": 5000,
    "branch": "Okhla",
    "address": "Delhi",
    "phone": "6666666666"
}

x8 = {
    "username": "user5",
    "password": "user5",
    "utype": "external-A",
    "firstname": "user5",
    "lastname": "Paliwal",
    "email": "user5@mail.com",
    "AC": "66666",
    "balance": 5000,
    "branch": "Okhla",
    "address": "Delhi",
    "phone": "5555555555"
}

x9 = {
    "username": "user6",
    "password": "user6",
    "utype": "external-A",
    "firstname": "user6",
    "lastname": "Paliwal",
    "email": "user6@mail.com",
    "AC": "77777",
    "balance": 5000,
    "branch": "Okhla",
    "address": "Delhi",
    "phone": "4444444444"
}

x10 = {
    "username": "user7",
    "password": "user7",
    "utype": "external-A",
    "firstname": "user7",
    "lastname": "Paliwal",
    "email": "user7@mail.com",
    "AC": "88888",
    "balance": 5000,
    "branch": "Okhla",
    "address": "Delhi",
    "phone": "3333333333"
}

x11 = {
    "username": "user8",
    "password": "user8",
    "utype": "external-A",
    "firstname": "user8",
    "lastname": "Paliwal",
    "email": "user8@mail.com",
    "AC": "99999",
    "balance": 5000,
    "branch": "Okhla",
    "address": "Delhi",
    "phone": "2222222222"
}

ulist = [x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11]

# if there is not already a user with username admin
# create a user with username admin and password = sha256("admin")
if User.objects().count() == 0:
    for i in ulist:
        createUser(i)
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
