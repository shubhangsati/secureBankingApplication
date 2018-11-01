from flask_cqlalchemy import CQLAlchemy
import uuid

db = CQLAlchemy()  # create a CQLAlchemy wrapper [uses cassandra-driver]


class PII(db.Model):
    uid = db.columns.Text(primary_key=True, required=True)
    first_name = db.columns.Text(required=True)
    last_name = db.columns.Text(required=True)
    email = db.columns.Text(required=True)
    address = db.columns.Text(required=True)
    mobile = db.columns.Text(required=True)


class User(db.Model):
    uid = db.columns.UUID(primary_key=True, default=uuid.uuid4)
    username = db.columns.Text(partition_key=True, required=True)
    password = db.columns.Text(required=True)
    otp_secret = db.columns.Text()
    otp_enabled = db.columns.Boolean(default=False)
    # boolean for two_way_login confirmation
    tw_login = db.columns.Boolean(default=False)
    # sessions established
    session_estd = db.columns.Boolean(default=False)

    # utype can be internal-A, internal-B, internal-C, external-A, or
    # external-B
    utype = db.columns.Text(required=True, default='external-A')


class Account(db.Model):
    uid = db.columns.Text(required=True)
    accountNumber = db.columns.Text(primary_key=True, required=True)
    balance = db.columns.Integer(required=True)
    bankBranch = db.columns.Text(required=True)


class Transaction(db.Model):
    transactionType = db.columns.TinyInt(required=True)
    transactionId = db.columns.UUID(primary_key=True, default=uuid.uuid4)
    sourceAC = db.columns.Text(required=True)
    destinationAC = db.columns.Text(required=True)
    amount = db.columns.Integer(required=True)
    time = db.columns.Text(required=True)
    approvalRequired = db.columns.Boolean(required=True)
    completed = db.columns.Boolean(required=True)


class PIIAprroval(db.Model):
    uid = db.columns.Text(primary_key=True, required=True)
    first_name = db.columns.Text(required=True)
    last_name = db.columns.Text(required=True)
    email = db.columns.Text(required=True)
    address = db.columns.Text(required=True)
    mobile = db.columns.Text(required=True)
    approved = db.columns.Boolean(required=True)


class Requests(db.Model):
    requestId = db.columns.UUID(primary_key=True, default=uuid.uuid4)
    # user who is initiating the request
    srcUid = db.columns.Text(required=True)
    dstUid = db.columns.Text(required=True)
    reqType = db.columns.Text(required=True)  # can be 'View', etc
    approved = db.columns.Boolean(required=True, default=False)
