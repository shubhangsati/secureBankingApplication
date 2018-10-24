# imports
from flask import Flask, render_template, request, url_for, redirect, session, flash
from functools import wraps
from models import db, User
import hashlib
import models

# create a new Flask app
app = Flask(__name__)
# load configurations from config.py
app.config.from_object("config.BaseConfig")
# initialize database
db.init_app(app)


# this function will be called whenever it is
# required to be logged in to be able to view a page
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
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
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

# logout route


@app.route("/logout")
@login_required
def logout():
    # pop information stored in the session
    session.pop('logged_in', None)
    session.pop('username', None)
    flash("You were just logged out!")
    return redirect(url_for('index'))

# test route to test the server


@app.route('/test')
def test():
    return "It works!"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
