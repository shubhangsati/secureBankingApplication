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

x5 = {
    "username": "admin",
    "password": "w7NkKa*XMCG6u2M@",
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
x6 = {
    "username": "admin1",
    "password": "PV3nil0vLDH*f*wV",
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
x7 = {
    "username": "admin2",
    "password": "inLzG&cUlg&tGf-s",
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
    "password": "XOEDN@ofM$Mvu3bT",
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

x1 = {
    "username": "user1",
    "password": "dXu!Y38CgXHEeJR8",
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

x2 = {
    "username": "user2",
    "password": "K*zWug^f2!WDxqI6",
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

x3 = {
    "username": "user3",
    "password": "tohL#6uuQho!njEa",
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

x4 = {
    "username": "user4",
    "password": "AfVLMXcw6y#VkKp3",
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

xA = {
    "username": "uXX",
    "password": "w7NkKa*XMCG1dsAGc",
    "utype": "external-A",
    "firstname": "Shubhang",
    "lastname": "Sati",
    "email": "user@securebank.com",
    "AC": "91824",
    "balance": 1000,
    "branch": "Okhla",
    "address": "Delhi",
    "phone": "9999999499"
}

xB = {
    "username": "uYY",
    "password": "w7NkKa*XMCG6u343",
    "utype": "external-A",
    "firstname": "Kartik",
    "lastname": "Mathur",
    "email": "kartik@securebank.com",
    "AC": "15125",
    "balance": 1000,
    "branch": "Okhla",
    "address": "Delhi",
    "phone": "9992199999"
}


ulist = [x0, x1, x2, x3, x4, x5, x6, x7]

createUser(xA)
createUser(xB)

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
