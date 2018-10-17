from flask import Flask, render_template, request, url_for, redirect, session, flash
from functools import wraps

app = Flask(__name__)
app.secret_key = "secret KEY"


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for("login"))
    return wrap


@app.route('/test')
def test():
    return "It works!"


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
        if request.form['username'] != 'admin' or request.form['password'] != 'password':
            error = 'Invalid credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash("You were just logged in!")
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route("/logout")
@login_required
def logout():
    session.pop('logged_in', None)
    flash("You were just logged out!")
    return ""


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
