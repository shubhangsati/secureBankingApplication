# imports
from flask import Flask, render_template, request, url_for, redirect, session, flash
from functools import wraps
from flask_socketio import SocketIO, emit
from models import *
from functions import *
from io import BytesIO
import hashlib
import models
import requests
import json
import pyotp
import pyqrcode
import datetime
from transactions import *

# create a new Flask app
app = Flask(__name__)
# load configurations from config.py
app.config.from_object("config.BaseConfig")
# initialize database
db.init_app(app)
# app.secret_key = "random"
# this function will be called whenever it is
# required to be logged in to be able to view a page

socketio = SocketIO(app)


@app.before_request
def before_request():
    now = datetime.datetime.now()
    try:
        last_active = session['last_active']
        delta = now - last_active
        if delta.seconds > 900:
            session['last_active'] = now
            flash("Session expired")
            return redirect(url_for("logout"))
    except BaseException:
        pass

    try:
        session['last_active'] = now
    except BaseException:
        pass


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and 'username' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for("login"))
    return wrap


def check_external(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and 'username' in session:
            if 'utype' in session and 'external' in session['utype']:
                return f(*args, **kwargs)
            else:
                return redirect(url_for('internal'))
        else:
            flash('You need to login as external user.')
            return redirect(url_for("logout"))
    return wrap


def check_internal(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and 'username' in session:
            if 'utype' in session and 'internal' in session['utype']:
                return f(*args, **kwargs)
            else:
                return redirect(url_for('index'))
        else:
            flash('You need to login as internal user.')
            return redirect(url_for("logout"))
    return wrap


# to-do as soon as tab closes - session destroyed

# default route

@app.route('/')
@login_required
@check_external
def index():
    current_user = session['username']
    row = models.User.objects(username=current_user)[0]
    if row.tw_login is False:
        flash('Two way authorization not completed. Login again.')
        destroy_session()
        return redirect(url_for('login'))
    # row.tw_login = False
    # row.save()

    details = fetchUserDetails(current_user)
    return render_template("index.html", details=details)

# login route
# uses both methods get and post


@app.route('/internal')
@login_required
@check_internal
def internal():
    current_user = session['username']
    row = models.User.objects(username=current_user)[0]
    if row.tw_login is False:
        flash('Two way authorization not completed. Login again.')
        destroy_session()
        return redirect(url_for('login'))
    pt = fetchPendingTransactions()
    piilist = viewPIIReq()
    return render_template('internal.html', pt=pt, piilist=piilist)


@app.route("/login", methods=["GET", "POST"])
def login():
    # session.permanent = True
    # check if user is logged in
    # load index page if user is logged in
    # Todo: add more checks
    if 'logged_in' in session and session['logged_in']:
        if 'external' in session['utype']:
            return redirect(url_for('index'))
        else:
            return redirect(url_for('internal'))

    # error string
    error = None
    if request.method == 'POST':
        # get username and password from form
        unameInput = request.form['username']
        passInput = request.form['password']
        captcha_response = request.form['g-recaptcha-response']
        if verify_captcha(captcha_response):
            # get row from database
            row = models.User.objects(username=unameInput)
            # if row count is 0 or password input from form
            # is not the same as that stored in the database return error
            if row.count() == 0 or hashlib.sha256(
                    passInput).hexdigest() != row[0].password:
                error = 'Invalid credentials. Please try again.'

            elif row[0].session_estd is True:
                flash("Session already open")

            # else log in successful
            else:
                session['logged_in'] = True
                session['username'] = unameInput
                session['login'] = 1
                session['utype'] = row[0].utype
                row[0].session_estd = True
                row[0].save()
                flash("You were just logged in!")
                # return redirect(url_for("index"))
                if row[0].otp_secret is None or row[0].otp_enabled is False:
                    return redirect(url_for('setup'))
                else:
                    return redirect(url_for('two_way_login'))
        else:
            flash("Invalid CAPTCHA!")
            return redirect(url_for('login'))

    return render_template('login.html', error=error,
                           sitekey=app.config['SITE_KEY'])


@app.route('/two_way_login', methods=["GET", "POST"])
@login_required
def two_way_login():

    if request.method == 'GET':
        if session['login'] == 1:
            session['login'] = 0
        else:
            return redirect(url_for('login'))

    if request.method == 'POST':
        token = request.form['token']
        current_user = session['username']
        row = models.User.objects(username=current_user)
        check_otp = row[0].otp_secret
        totp = pyotp.TOTP(check_otp)
        if(totp.verify(token)):
            row[0].tw_login = True
            row[0].save()
            flash("Login successful")
            if 'external' in session['utype']:
                return redirect(url_for('index'))
            else:
                return redirect(url_for('internal'))

        else:
            flash("Invalid Otp! Try again")
            return redirect(url_for('login'))

    return render_template('two_way_login.html')


@app.route('/setup', methods=["GET", "POST"])
@login_required
def setup():

    if request.method == 'GET':
        if session['login'] == 1:
            session['login'] = 0
        else:
            return redirect(url_for('login'))

    if request.method == 'POST':
        token = request.form['token']
        current_user = session['username']
        destroy_session()
        row = models.User.objects(username=current_user)[0]
        check_otp = row.otp_secret
        totp = pyotp.TOTP(check_otp)
        if(totp.verify(token)):
            row.otp_enabled = True
            row.save()
            flash("Otp registration successful. Please login again")
            return redirect(url_for('login'))
        else:
            flash("Invalid Otp!! Verification Unsuccessful. Try again")
            return redirect(url_for('login'))
    return render_template('otp_qrcode.html'), 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@app.route('/qrcode')
@login_required
def qrcode():

    current_user = session['username']
    row = models.User.objects(username=current_user)[0]
    if(row.otp_enabled is True):
        return redirect(url_for('login'))

    # render qrcode for google authenticator
    url = pyqrcode.create(get_totp_uri(current_user))
    stream = BytesIO()
    url.svg(stream, scale=3)
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


def get_totp_uri(current_user):
    secret_base32 = pyotp.random_base32()
    totp = pyotp.TOTP(secret_base32)
    # secret_base for Otp written in the database
    row = models.User.objects(username=current_user)[0]
    row.otp_secret = secret_base32
    row.save()

    return 'otpauth://totp/SBS:{0}?secret={1}&issuer=SBS' \
        .format(current_user, secret_base32)


def verify_captcha(captcha_response):
    secret = "6LcSb3cUAAAAACi3usSfmugL4L94lt0plD6Yb5Vv"
    payload = {'response': captcha_response, 'secret': secret}
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success']

# logout route


@app.route("/logout")
@login_required
def logout():
    # pop information stored in the session
    destroy_session()
    flash("You were just logged out!")
    return redirect(url_for('login'))


def destroy_session():
    current_user = session['username']
    row = models.User.objects(username=current_user)[0]
    row.session_estd = False
    row.tw_login = False
    row.save()
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('login', None)


"""@socketio.on('disconnect')
def disconnect_user():
    destroy_session()
    session.pop('yourkey', None)"""

# test route to test the server


@app.route('/test')
def test():
    return "It works!"


@app.route('/quicktransfer', methods=['POST'])
@login_required
@check_external
def quicktransfer():
    otp_result = verifyOTP()
    if otp_result is not True:
        flash(otp_result)
        return redirect(url_for('index'))

    if 'destinationAC' in request.form:
        destinationAC = request.form['destinationAC']
    else:
        flash('destination account not set')
        return redirect(url_for('index'))

    if 'amount' in request.form:
        amount = request.form['amount']
    else:
        flash('amount not set')
        return redirect(url_for('index'))

    user = User.objects(username=session['username'])[0]
    sourceAC = Account.objects(uid=user.uid).allow_filtering()[0]
    result = createTransactionRecord(1, amount, destinationAC,
                                     sourceAC.accountNumber)
    if not result[0]:
        flash('Invalid input')
        return redirect(url_for('index'))
    if result[1]:
        flash('Critical Transaction! Sent for review')
        return redirect(url_for('index'))
    if result[2]:
        flash('Transaction Completed')
        return redirect(url_for('index'))
    if not result[2]:
        flash('Transaction failed')
        return redirect(url_for('index'))

    return redirect(url_for('index'))


@app.route('/debit', methods=['POST'])
@login_required
@check_external
def debitMoney():
    otp_result = verifyOTP()
    if otp_result is not True:
        flash(otp_result)
        return redirect(url_for('index'))

    if 'amount' in request.form:
        amount = request.form['amount']
    else:
        flash('amount not set')
        return redirect(url_for('index'))

    user = User.objects(username=session['username'])[0]
    sourceAC = Account.objects(uid=user.uid).allow_filtering()[0]
    result = createTransactionRecord(2, amount, sourceAC.accountNumber)
    if not result[0]:
        flash('Invalid input')
        return redirect(url_for('index'))
    if result[1]:
        flash('Critical Transaction! Sent for review')
        return redirect(url_for('index'))
    if result[2]:
        flash('Transaction Completed')
        return redirect(url_for('index'))
    if not result[2]:
        flash('Transaction failed')
        return redirect(url_for('index'))

    return redirect(url_for('index'))


@app.route('/credit', methods=['POST'])
@login_required
@check_external
def creditMoney():
    otp_result = verifyOTP()
    if otp_result is not True:
        flash(otp_result)
        return redirect(url_for('index'))

    if 'amount' in request.form:
        amount = request.form['amount']
    else:
        flash('amount not set')
        return redirect(url_for('index'))

    user = User.objects(username=session['username'])[0]
    sourceAC = Account.objects(uid=user.uid).allow_filtering()[0]
    result = createTransactionRecord(3, amount, sourceAC.accountNumber)
    if not result[0]:
        flash('Invalid input')
        return redirect(url_for('index'))
    if result[1]:
        flash('Critical Transaction! Sent for review')
        return redirect(url_for('index'))
    if result[2]:
        flash('Transaction Completed')
        return redirect(url_for('index'))
    if not result[2]:
        flash('Transaction failed')
        return redirect(url_for('index'))

    return redirect(url_for('index'))


@app.route('/PIImod', methods=['POST'])
@login_required
@check_external
def PIImod():
    otp_result = verifyOTP()
    if otp_result is not True:
        flash(otp_result)
        return redirect(url_for('index'))

    required = {
        'firstname': None,
        'lastname': None,
        'email': None,
        'address': None,
        'phone': None}
    for i in required:
        if i not in request.form:
            flash_message = '[-] ' + i + ' not set'
            flash(flash_message)
            return redirect(url_for('index'))
        else:
            required[i] = request.form[i]

    result = updatePII(session['username'], required['firstname'],
                       required['lastname'], required['email'],
                       required['address'], required['phone'])

    if result:
        flash("PII update -- request created")
    else:
        flash("Invalid input")
    return redirect(url_for('index'))


@app.route('/approveTransaction', methods=['POST'])
@login_required
@check_internal
def approveTransaction1():
    if 'approveTransactionIndex' in request.form:
        approveIndex = request.form['approveTransactionIndex']
    else:
        flash('Invalid')
        return redirect(url_for('internal'))

    if is_int(approveIndex):
        approveIndex = int(approveIndex) - 1

    result = approveTransaction(approveIndex)
    if result:
        flash("Transaction -- Approved")
    else:
        flash("Invalid input")
    return redirect(url_for('internal'))


@app.route('/approvePII', methods=['POST'])
@login_required
@check_internal
def approvePII1():
    if 'approvePIIIndex' in request.form:
        approveIndex = request.form['approvePIIIndex']
    else:
        flash('Invalid')
        return redirect(url_for('internal'))
    if is_int(approveIndex):
        approveIndex = int(approveIndex) - 1
    result = approvePII(approveIndex)
    if result:
        flash("PII update -- Approved")
    else:
        flash("Invalid input")
    return redirect(url_for('internal'))


@app.route('/viewTransactions', methods=['POST'])
@login_required
@check_internal
def viewTransaction():
    if 'acnumber' in request.form:
        acnumber = request.form['acnumber']
        viewtransactions = ViewTransactions(acnumber)
        # get transactions
        pt = fetchPendingTransactions()
        piilist = viewPIIReq()
        return render_template(
            'internal.html', pt=pt, piilist=piilist, vt=viewtransactions, tab="transactions")
    else:
        flash('Invalid')
        return redirect(url_for('internal'))


@app.route('/deleteUser', methods=['POST'])
@login_required
@check_internal
def delUser():
    otp_result = verifyOTP()
    if otp_result is not True:
        flash(otp_result)
        return redirect(url_for('internal'))

    if session['utype'] != 'externalC':
        flash('Function not allowed')
        return redirect(url_for('internal'))

    if 'acnumber' in request.form:
        acnumber = request.form['acnumber']
        account = Account.objects(accountNumber=acnumber)
        userID = None
        if account.count() > 0:
            userID = account[0].uid
        else:
            flash('Invalid Input')
            return redirect(url_for('internal'))
        deleteUser(userID)
        flashmessage = 'User with account number: ' + acnumber + ' has been deleted'
        flash(flashmessage)
        return redirect(url_for('internal'))
    else:
        flash('Invalid')
        return redirect(url_for('internal'))
    return redirect(url_for('internal'))


@app.route('/viewlast10transactions', methods=['POST'])
@login_required
@check_external
def viewlast10transactions():
    otp_result = verifyOTP()
    if otp_result is not True:
        flash(otp_result)
        return redirect(url_for('index'))

    userid = User.objects(username=session['username'])[0].uid
    acnumber = Account.objects(uid=userid).allow_filtering()[0].accountNumber
    allTransactions = ViewTransactions(acnumber)

    def compareTransactions(t1, t2):
        time1 = datetime.datetime.strptime(t1.time, '%c')
        time2 = datetime.datetime.strptime(t2.time, '%c')
        if time1 < time2:
            return -1
        if time1 == time2:
            return 0
        if time1 > time2:
            return 1

    allTransactions.sort(cmp=compareTransactions, reverse=True)
    last10transactions = allTransactions[:10]
    details = fetchUserDetails(session['username'])
    return render_template("index.html", details=details,
                           last10transactions=last10transactions,
                           currenttab='transactions_last10transactions')


def verifyOTP():
    if 'token' not in request.form:
        return 'Enter OTP'

    otp = request.form['token']
    secret = User.objects(username=session['username'])[0].otp_secret
    totp = pyotp.TOTP(secret)
    if not totp.verify(otp):
        return 'Incorrect OTP'

    return True


def is_int(n):
    try:
        int(n)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    app.run(host="0.0.0.0")
