from flask_cqlalchemy import CQLAlchemy
import uuid

db = CQLAlchemy()  # create a CQLAlchemy wrapper [uses cassandra-driver]


class User(db.Model):
    uid = db.columns.UUID(primary_key=True, default=uuid.uuid4)
    username = db.columns.Text(partition_key=True, required=True)
    password = db.columns.Text(required=True)
    otp_secret = db.columns.Text()
    otp_enabled = db.columns.Boolean(default=False)


class Account(db.Model):
    uid = db.columns.Text(required=True)
    accountNumber = db.columns.Integer(primary_key=True, required=True)
    balance = db.columns.Integer(required=True)
    bankBranch = db.columns.Text(required=True)


class Transaction(db.Model):
    transactionType = db.columns.TinyInt(required=True)
    transactionId = db.columns.Text(primary_key=True, required=True)
    sourceAC = db.columns.Integer(required=True)
    destinationAC = db.columns.Integer(required=True)
    amount = db.columns.Integer(required=True)
    time = db.columns.DateTime(required=True)
