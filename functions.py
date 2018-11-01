from models import *
#from app import app
from sanitize import *

# db.init_app(app)  # initializes database
# 
# db.create_keyspace_simple('SBS', 1)  # creates keyspace if does not exist
# 
# db.sync_db()

# this function takes in uid and deletes the fields associated with him
# this would delete all pending requests, transactions, accounts
# associated with that user


def createUser(x): # expects x as dict
    User.create(username=x["username"], password=x["password"], utype=x["utype"])
    id = User.objects(username=x["username"]).allow_filtering()[0].uid
    PII.create(uid=id, first_name=x["firstname"], last_name=x["lastname"], email=x["email"], address=x["address"], mobile=x["phone"])
    Account.create(uid=id, accountNumber=x["AC"], balance=x["balance"], bankBranch=x["branch"])

def deleteUser(userID):

    user = User.objects(uid=userID).allow_filtering()
    for x in user:
        User.delete(x)

    pii = PII.objects(uid=userID).allow_filtering()
    for x in pii:
        PII.delete(x)

    account = Account.objects(uid=userID).allow_filtering()
    AC = account[0].accountNumber
    for x in account:
        Account.delete(x)

    transaction1 = Transaction.objects(sourceAC=AC).allow_filtering()
    for x in transaction1:
        Transaction.delete(x)

    transaction2 = Transaction.objects(destinationAC=AC).allow_filtering()
    for x in transaction2:
        Transaction.delete(x)

    requests1 = Requests.objects(srcUid=userID).allow_filtering()
    for x in requests1:
        Requests.delete(x)

    requests2 = Request.objects(dstUid=userID).allow_filtering()
    for x in requests2:
        Requests.delete(x)

    piiapproval = Request.objects(uid=userID).allow_filtering()
    for x in piiapproval:
        PIIApproval.delete(x)


def ViewTransactions(AC):
    t1 = Transaction.objects.filter(sourceAC=AC).allow_filtering()
    views = []
    for x in t1:
        views.append(x)
    t2 = Transaction.objects.filter(destinationAC=AC).allow_filtering()
    for x in t2:
        views.append(x)
    return views
