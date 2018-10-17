from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)


@app.route('/test')
def test():
    return "It works!"


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'password':
            error = 'Invalid credentials. Please try again.'
        else:
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
