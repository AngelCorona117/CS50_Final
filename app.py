import os
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///store.db")

db.execute(
    "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, hash TEXT NOT NULL, money MONEY DEFAULT 10000.00);"
)

app.config["SECRET_KEY"] = "asdkasjfñlsdkfjslffyjypñ45604693045'34853'9429592457"


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/black", methods=["GET"])
def black():
    return render_template("black.html")


@app.route("/white", methods=["GET"])
def white():
    return render_template("white.html")


@app.route("/newReleases", methods=["GET"])
def newReleases():
    return render_template("newReleases.html")


@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html")


@app.route("/shopping", methods=["GET"])
def shopping():
    return render_template("shopping.html")


@app.route("/user", methods=["GET", "POST"])
def user():
    if request.method == "GET":

        return render_template("user.html")
    
    elif request.method == "POST":
        if request.form["submit_button"] == "login":

            print(request.form["submit_button"])
            # ensure correct usage
            loginUsername = request.form.get("login-username")
            loginPassword = request.form.get("login-password")

            if not loginUsername or not loginPassword:
                flash("Must provide a username and a password", "danger")
                return redirect(url_for("user"))

            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE username = ?", loginUsername)

            # password compare returns true if both passwords match
            try:
                passwordCompare = check_password_hash(rows[0]["hash"], loginPassword)
            except:
                flash("None users found", "warning")
                return redirect(url_for("user"))

            # if passwords dont match or there is more than 1 user with that name
            if len(rows) > 1 or passwordCompare == False:
                flash("None user found", "warning")
                return redirect(url_for("user"))

            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]
            flash("You were logged in", "success")

            return redirect(url_for("user"))

        elif request.form["submit_button"] == "register":

            username = request.form.get("register-username")
            password = request.form.get("register-password")
            confirmation = request.form.get("register-confirmation")

            # ensure correct usage
            if not username or not password:
                flash("Incorrect usage, please provide a password and a username", "danger")
                return redirect(url_for("user"))
            
            elif confirmation != password:
                flash("Password and confirmation do not match", "warning")
                return redirect(url_for("user"))

            # hash the password for security purpouses
            hashedPassword = generate_password_hash(password)

            # if the user provided a  valid password and a username
            userId = db.execute("SELECT id FROM users WHERE username=?;", username)

            # ensure name is not taken
            if len(userId) > 0:
                flash("Username already taken", "info")
                return redirect(url_for("user"))

            # user provided a non taken user and a password, register user
            db.execute(
                "INSERT INTO users (username, hash) VALUES (? , ?);",
                username,
                hashedPassword,
            )

            # Remember which user has logged in
            session["user_id"] = userId
            flash("Congrats! You were registered", "success")

            return redirect(url_for("user"))

        return redirect(url_for("user"))



@app.route("/logout", methods=["GET"])
def logout():
    if "user_id" in session:
        session.clear()
        flash(f"You were logged out", "success")
        return redirect(url_for("home"))

    flash("You are not logged in", "info")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
