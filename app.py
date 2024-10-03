from cs50 import SQL
from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from helpers import login_required
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect to sqlite database
db = SQL("sqlite:///tms.db")

@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login() :
    
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            return render_template("error.html")

        # Ensure password was submitted
        elif not password:
            return render_template("error.html")
        
        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", username
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password"], password
        ):
            return render_template("error.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        print("Successfully logged in")

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("login.html")
    

