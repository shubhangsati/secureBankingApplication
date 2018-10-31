# imports
from flask import Flask, render_template, request, url_for, redirect, session, flash
from functools import wraps
from models import db, User
from io import BytesIO
import hashlib
import models
import requests
import json
import pyotp
import pyqrcode

# create a new Flask app
app = Flask(__name__)
# load configurations from config.py
app.config.from_object("config.BaseConfig")
# initialize database
db.init_app(app)
# app.secret_key = "random"
# this function will be called whenever it is
# required to be logged in to be able to view a page


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and 'username' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for("login"))
    return wrap

# default route


@app.route('/')
@login_required
def index():
    return render_template("index.html")

# login route
# uses both methods get and post


@app.route("/login", methods=["GET", "POST"])
def login():
    # check if user is logged in
    # load index page if user is logged in
    # Todo: add more checks
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for("index"))

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

            # else log in successful
            else:
                session['logged_in'] = True
                session['username'] = unameInput
                flash("You were just logged in!")
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
    if request.method == 'POST':
        token = request.form['token']
        current_user = session['username']
        row = models.User.objects(username=current_user)
        check_otp = row[0].otp_secret
        totp = pyotp.TOTP(check_otp)
        if(totp.verify(token)):
            return redirect(url_for('index'))
        else:
            flash("Invalid Otp! Try again")
            return redirect(url_for('two_way_login'))

    return render_template('two_way_login.html')


@app.route('/setup', methods=["GET", "POST"])
@login_required
def setup():
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
            # return redirect(url_for('login'))
        else:
            flash("Invalid Otp!! Verification Unsuccessful. Try again")
            return redirect(url_for('setup'))
    return render_template('otp_qrcode.html'), 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@app.route('/qrcode')
@login_required
def qrcode():
    current_user = session['username']

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
    return redirect(url_for('index'))


def destroy_session():
    session.pop('logged_in', None)
    session.pop('username', None)

# test route to test the server


@app.route('/test')
def test():
    return "It works!"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
