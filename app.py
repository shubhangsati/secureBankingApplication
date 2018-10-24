import uuid
from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_cqlalchemy import CQLAlchemy
from functools import wraps
import hashlib
import models

app = Flask(__name__)
app.config.from_object("config.BaseConfig")
db = CQLAlchemy(app)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for("login"))
    return wrap


@app.route('/')
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for("index"))

    error = None
    if request.method == 'POST':
        unameInput = request.form['username']
        passInput = request.form['password']
        row = models.User.objects(username=unameInput)
        if row.count() == 0 or hashlib.sha256(
                passInput).hexdigest() != row[0].password:
            error = 'Invalid credentials. Please try again.'

        else:
            session['logged_in'] = True
            session['username'] = unameInput
            flash("You were just logged in!")
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route("/logout")
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash("You were just logged out!")
    return redirect(url_for('index'))


@app.route('/test')
def test():
    return "It works!"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
