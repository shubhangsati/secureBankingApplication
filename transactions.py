from models import *
from app import app
from sanitize import *
import time

db.init_app(app)  # initializes database

db.create_keyspace_simple('SBS', 1)  # creates keyspace if does not exist

db.sync_db()

# accepts an object of type Transaction
# type can be 1, 2 or 3
# 1 is transfer
# 2 is debit, source is BANK for this option
# 3 is credit, source is BANK for this option


def createTransactionRecord(type, amt, destination, source="BANK"):
    flag = False
    source = clean(source)
    destination = clean(destination)
    f1 = Account.objects(accountNumber=destination).count() == 1
    if source != "BANK":
        f2 = Account.objects(accountNumber=destination).count() == 1
    else:
        f2 = True
    if check_amount(amt) and f1 and f2:
        flag = True
        critical = False
        if amt >= 100000:
            critical = True

        transaction = Transaction.create(
            transactionType=type,
            sourceAC=source,
            destinationAC=destination,
            amount=amt,
            time=time.asctime(),
            approvalRequired=critical)

        if not critical:
            if type == 1:
                transfer(transaction)
            elif type == 2:
                debit(transaction)
            elif type == 3:
                credit(transaction)

    return flag


def tranfer(transaction):
    src = Account.objects(accountNumber=transaction.sourceAC)[0]
    dst = Account.objects(accountNumber=transaction.destinationAC)[0]
    amt = transaction.amount
    completed = transaction.completed

    if not completed:
        s = src.balance
        d = dst.balance
        if amount <= s:
            d += amount
            s -= amount
            src.update(amount=s)
            dst.update(amount=d)
            transaction.completed = True

    return transaction.completed


def debit(transaction):
    dst = Account.objects(accountNumber=transaction.destinationAC)[0]
    amt = transaction.amount
    completed = transaction.completed

    if not completed:
        d = dst.balance
        if amount <= d:
            d -= amount
            dst.update(amount=d)
            transaction.completed = True

    return transaction.completed


def credit():
    dst = Account.objects(accountNumber=transaction.destinationAC)[0]
    amt = transaction.amount
    completed = transaction.completed

    if not completed:
        d = dst.balance
        d += amount
        dst.update(amount=d)
        transaction.completed = True

    return transaction.completed
