from models import *
# from app import app
from sanitize import *
from hashlib import sha256
from transactions import *

# db.init_app(app)  # initializes database
#
# db.create_keyspace_simple('SBS', 1)  # creates keyspace if does not exist
#
# db.sync_db()

# this function takes in uid and deletes the fields associated with him
# this would delete all pending requests, transactions, accounts
# associated with that user


def updatePII(uname, fname, lname, mail, add, phone):
    flag = False
    row = User.objects(username=uname).allow_filtering()
    if row.count() == 1:
        id = row[0].uid
        PIIApproval.create(
            uid=id,
            first_name=fname,
            last_name=lname,
            email=mail,
            address=add,
            mobile=phone,
            approved=False)
        flag = True

    return flag


def createUser(x):  # expects x as dict
    flag = False
    # print type(Account.objects(accountNumber=x["AC"]).count())
    if Account.objects(accountNumber=x["AC"]).count() == 0:
        print 'temp'
        User.create(
            username=x["username"],
            password=sha256(
                x["password"]).hexdigest(),
            utype=x["utype"])
        id = User.objects(username=x["username"]).allow_filtering()[0].uid

        if 'external' in x["utype"]:

            PII.create(
                uid=id,
                first_name=x["firstname"],
                last_name=x["lastname"],
                email=x["email"],
                address=x["address"],
                mobile=x["phone"])

            Account.create(
                uid=id,
                accountNumber=x["AC"],
                balance=x["balance"],
                bankBranch=x["branch"])

        flag = True

    return flag


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

def approveTransaction(trancId):
    row = Transaction.objects(transactionId=trancId).allow_filtering()[0]


def viewPIIReq():
    pii = PIIApproval.objects().allow_filtering()
    views=[]
    for x in pii:
        view.append(x)
    return views

# approvePII takes in index
def approvePII(i):
    temp = viewPIIReq()
    pii = temp[i]
    ID = pii.uid
    PII.delete(pii)
    PII.create
    uname = User.objects(uid=ID)[0].username
    pii.updatePII(uname, pii.first_name, pii.last_name, )

    return 

def fetchUserDetails(uname):
    user = User.objects(username=uname)[0]
    pii = PII.objects(uid=user.uid).allow_filtering()[0]
    account = Account.objects(uid=user.uid).allow_filtering()[0]
    details = {}
    details["firstname"] = pii.first_name
    details["lastname"] = pii.last_name
    details["ac"] = account.accountNumber
    details["balance"] = account.balance
    details["email"] = pii.email
    details["address"] = pii.address
    details["phone"] = pii.mobile
    details["utype"] = user.utype
    details["branch"] = account.bankBranch
    return details
