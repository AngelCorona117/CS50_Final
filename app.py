import os
from cs50 import SQL
from config import Config
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///store.db")

db.execute(
    "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, hash TEXT NOT NULL, money MONEY DEFAULT 10000.00);"
)

app = Flask(__name__)
app.config.from_object(Config)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        # get the 15 most recent products

        rows = db.execute("SELECT * FROM products;")

        return render_template("home.html", rows=rows)
    if request.method == "POST":
        if request.form.get("buy") == "buyed":
            item = request.form.get("selected-item")
            session["item"] = item

            return redirect(url_for("item"))

        filtered = request.form.get("filter")
        filtered = filtered.split("|")
        filteredValue = filtered[0]
        filteredType = filtered[1]

        if filteredType == "price":
            rows = db.execute(
                f"SELECT * FROM products ORDER BY {filteredType} {filteredValue}, year_of_release ASC ;"
            )
        else:
            rows = db.execute(
                f"SELECT * FROM products WHERE {filteredType} = '{filteredValue}' ORDER BY year_of_release DESC ;"
            )

        return render_template("home.html", rows=rows)


@app.route("/newReleases", methods=["GET", "POST"])
def newReleases():
    if request.method == "GET":
        # get the 15 most recent products

        rows = db.execute(
            "SELECT * FROM products ORDER BY year_of_release DESC LIMIT 15 ;"
        )

        return render_template("newReleases.html", rows=rows)

    if request.form.get("buy") == "buyed":
        item = request.form.get("selected-item")
        session["item"] = item

        return redirect(url_for("item"))

    filtered = request.form.get("filter")
    filtered = filtered.split("|")
    filteredValue = filtered[0]
    filteredType = filtered[1]

    if filteredType == "price":
        rows = db.execute(
            f"SELECT * FROM products ORDER BY {filteredType} {filteredValue}, year_of_release ASC LIMIT 15;"
        )
    else:
        rows = db.execute(
            f"SELECT * FROM products WHERE {filteredType} = '{filteredValue}' ORDER BY year_of_release DESC LIMIT 15;"
        )

    return render_template("newReleases.html", rows=rows)


@app.route("/item", methods=["GET", "POST"])
def item():
    if not "user_id" in session:
        flash("Log in to add items to your cart", "info")
        return redirect(url_for("home"))

    if not "item" in session:
        flash("Select an item to view", "info")
        return redirect(url_for("home"))
    
    #get the last clicked item
    item = session["item"]

    if request.method == "GET":

        # get the last product the user clicked
        item = db.execute("SELECT * FROM products WHERE id = ?", item)[0]

        return render_template("item.html", item=item)

    size = request.form.get("size")
    ammount = request.form.get("ammount")
    stock = db.execute("SELECT stock FROM products WHERE id = ?", item)[0]["stock"]

    # ensure correct usage
    if not size or not ammount:
        flash("Select a size and a quantity", "danger")
        return redirect(url_for("item"))

    try:
        ammount = int(ammount)
    except:
        flash("Select a valid quantity", "danger")
        return redirect(url_for("item"))

    if ammount < 1:
        flash("Select a valid quantity", "danger")
        return redirect(url_for("item"))

    if ammount > stock:
        flash("Not enough stock", "danger")
        return redirect(url_for("item"))

    # check if the user has any other item of the same type in the cart
    cart = db.execute(
        "SELECT * FROM cart WHERE user_id = ? AND product_id = ?  AND measure= ?",
        session["user_id"],
        item,
        size,
    )
    if len(cart) >= 1:
        # update the quantity of the item in the cart
        actualAmmount = cart[0]["quantity"]
        newAmmount = actualAmmount + ammount

        if newAmmount > stock:
            flash("Not enough stock", "danger")
            return redirect(url_for("item"))

        db.execute(
            "UPDATE cart SET quantity = ? WHERE user_id = ? AND product_id = ?",
            newAmmount,
            session["user_id"],
            item,
        )
        flash("Items owned updated", "success")
        return redirect(url_for("home"))

    # add the item to the cart if the user does not have any of that size
    price = db.execute("SELECT price FROM products WHERE id = ?", item)[0]["price"]

    db.execute(
        "INSERT INTO cart (user_id, product_id, quantity, measure, price) VALUES (?, ?, ?, ?, ?)",
        session["user_id"],
        item,
        ammount,
        size,
        price,
    )
    flash("Item added to cart", "success")
    return redirect(url_for("home"))


@app.route("/shopping", methods=["GET", "POST"])
def shopping():
    db.execute(
        "CREATE TABLE IF NOT EXISTS cart (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL, measure VARCHAR(5) NOT NULL, price MONEY NOT NULL,   FOREIGN KEY (user_id) REFERENCES users(id), FOREIGN KEY (product_id) REFERENCES products(id));"
    )

    if not "user_id" in session:
        flash("Log in to add items to your cart", "info")
        return redirect(url_for("home"))

    money = db.execute("SELECT money FROM users WHERE id = ?", session["user_id"])[0][
        "money"
    ]

    rows = db.execute(
        "SELECT cart.*, image_path, name from products INNER JOIN cart ON products.id = cart.product_id WHERE cart.user_id = ?",
        session["user_id"],
    )
    if len(rows) == 0:
        flash("Your cart is empty", "info")
        return redirect(url_for("home"))

    totalCost = 0
    for row in rows:
        quantity = row["quantity"]
        price = row["price"]
        totalCost += quantity * price
    totalCost = round(totalCost, 2)

    if request.method == "GET":
        # select image from products and everything from cart and join them

        return render_template(
            "shopping.html",
            rows=rows,
            money=money,
            totalCost=totalCost,
        )

    # check if the user has enough money
    if totalCost > money:
        flash("Not enough money", "danger")
        return render_template(
            "shopping.html",
            rows=rows,
            money=money,
            totalCost=totalCost,
        )

    # if he has enough money, update the money and delete the items from the cart+update the stock
    newMoney = money - totalCost
    db.execute("UPDATE users SET money = ? WHERE id = ?", newMoney, session["user_id"])

    # update the stock of those items
    for row in rows:
        item = row["product_id"]
        quantity = row["quantity"]
        stock = db.execute("SELECT stock FROM products WHERE id = ?", item)[0]["stock"]
        newStock = stock - quantity
        db.execute("UPDATE products SET stock = ? WHERE id = ?", newStock, item)

    # delete the items from the cart
    db.execute("DELETE FROM cart WHERE user_id = ?", session["user_id"])

    flash("Purchase completed", "success")
    return redirect(url_for("home"))


@app.route("/user", methods=["GET", "POST"])
def user():
    if request.method == "GET":
        try:
            if session["user_id"]:
                # if the user is logged in display his info
                loggedUsername = db.execute(
                    "SELECT username FROM users WHERE id = ?", session["user_id"]
                )
                loggedMoney = db.execute(
                    "SELECT money FROM users WHERE id = ?", session["user_id"]
                )
                loggedUsername = loggedUsername[0]["username"]
                loggedMoney = loggedMoney[0]["money"]
                loggedMoney = round(loggedMoney, 2)

                return render_template(
                    "user.html", loggedUsername=loggedUsername, loggedMoney=loggedMoney
                )
        except:
            return render_template("user.html")

    elif request.method == "POST":
        # if the user is trying to login
        if request.form["submit_button"] == "login":
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

        # if the user is trying to register
        elif request.form["submit_button"] == "register":
            username = request.form.get("register-username")
            password = request.form.get("register-password")
            confirmation = request.form.get("register-confirmation")

            # ensure correct usage
            if not username or not password:
                flash(
                    "Incorrect usage, please provide a password and a username",
                    "danger",
                )
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

            userId = db.execute("SELECT id FROM users WHERE username=?;", username)
            userId = userId[0]["id"]
            # Remember which user has logged in
            session["user_id"] = userId
            flash("Congrats! You were registered", "success")

            return redirect(url_for("user"))

        # if the user is trying to update his username
        elif request.form["submit_button"] == "update-username":
            # ensure correct usage
            newUsername = request.form.get("update-username")

            if not newUsername:
                flash("Must provide a username", "danger")
                return redirect(url_for("user"))

            oldUsername = db.execute(
                "SELECT username FROM users WHERE id = ?", session["user_id"]
            )
            oldUsername = oldUsername[0]["username"]

            if newUsername == oldUsername:
                flash("You already have that username", "info")
                return redirect(url_for("user"))

            # ensure name is not taken
            if (
                len(db.execute("SELECT id FROM users WHERE username=?;", newUsername))
                > 0
            ):
                flash("Username already taken", "warning")
                return redirect(url_for("user"))

            # update username
            db.execute(
                "UPDATE users SET username = ? WHERE id = ?",
                newUsername,
                session["user_id"],
            )
            flash(f"Username updated", "success")

            return redirect(url_for("user"))

        # if the user is trying to update his password
        elif request.form["submit_button"] == "update-password":
            oldpassword = request.form.get("old-password")
            newpassword = request.form.get("update-password")
            confirmation = request.form.get("update-confirmation")

            # ensure correct usage
            if not oldpassword or not newpassword or not confirmation:
                flash(
                    "Must provide old password, new password and a confirmation",
                    "danger",
                )
                return redirect(url_for("user"))

            elif len(newpassword) < 8:
                flash("Password must be at least 8 characters", "danger")
                return redirect(url_for("user"))

            elif oldpassword == newpassword:
                flash("Old password and new password must be different", "warning")
                return redirect(url_for("user"))

            elif confirmation != newpassword:
                flash("Password and confirmation do not match", "warning")
                return redirect(url_for("user"))

            # Query database for username
            currentPassword = db.execute(
                "SELECT hash FROM users WHERE id = ?", session["user_id"]
            )

            # password compare returns true if both passwords match

            if not check_password_hash(currentPassword[0]["hash"], oldpassword):
                flash("Old password do not match, please try again", "warning")
                return redirect(url_for("user"))

            elif oldpassword == newpassword:
                flash("Old password and new password must be different", "warning")
                return redirect(url_for("user"))

            # if passwords match, update password
            newpassword = generate_password_hash(newpassword)
            db.execute(
                "UPDATE users SET hash = ? WHERE id = ?",
                newpassword,
                session["user_id"],
            )
            flash("Password updated", "success")
            return redirect(url_for("user"))

        # if the user is trying to update his money
        elif request.form["submit_button"] == "update-money":
            # ensure correct usage
            newMoney = request.form.get("update-money")

            if not newMoney:
                flash("Must provide an amount of money", "danger")
                return redirect(url_for("user"))

            newMoney = float(newMoney)

            if newMoney < 0:
                flash("Must provide a positive number", "danger")
                return redirect(url_for("user"))

            if newMoney > 10000:
                flash("Must provide a number less than ten thousand dollars", "warning")
                return redirect(url_for("user"))

            oldMoney = db.execute(
                "SELECT money FROM users WHERE id = ?", session["user_id"]
            )
            oldMoney = float(oldMoney[0]["money"])

            if oldMoney > 1000000:
                flash("You have reached your credit limit", "info")
                return redirect(url_for("user"))

            # everything worked as supposed to, update money
            updatedMoney = oldMoney + newMoney

            db.execute(
                "UPDATE users SET money = ? WHERE id = ?",
                updatedMoney,
                session["user_id"],
            )
            flash("Balance updated", "success")
            return redirect(url_for("user"))
        
        elif request.form["submit_button"] == "update-stock-button":

            itemID= request.form.get("update-stock-id")
            itemQuantity = request.form.get("update-stock")

            # ensure correct usage
            if not itemID or not itemQuantity:
                flash("Must provide an item ID and a quantity", "danger")
                return redirect(url_for("user"))
            
            try:
                itemID = int(itemID)
                itemQuantity = int(itemQuantity)
            except:
                flash("Must provide a valid item ID and a quantity", "danger")
                return redirect(url_for("user"))
            
            if itemQuantity < 0:
                flash("Must provide a positive quantity", "danger")
                return redirect(url_for("user"))
            
            if itemQuantity > 100:
                flash("Must provide a quantity less than 100", "warning")
                return redirect(url_for("user"))
            
            # ensure item exists
            item = db.execute("SELECT * FROM products WHERE id = ?", itemID)

            if len(item) != 1:
                flash("product does not exist", "warning")
                return redirect(url_for("user"))
            
            #update stock
            oldStock=item[0]["stock"]
            newStock=oldStock+itemQuantity

            db.execute("UPDATE products SET stock = ? WHERE id = ?", newStock, itemID)
            flash("Stock updated", "success")
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
