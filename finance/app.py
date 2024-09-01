import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    portfolio = db.execute("SELECT id, symbol, SUM(shares) FROM trades WHERE id = ? GROUP BY symbol HAVING SUM(shares) > 0 ORDER BY price DESC", session["user_id"])

    cash = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

    stock_value = 0

    for stock in portfolio:
        stock_data = lookup(stock["symbol"])
        stock["currentprice"] = stock_data["price"]
        stock["totalprice"] = stock_data["price"] * stock["SUM(shares)"]
        stock_value += stock["totalprice"]

    return render_template("index.html", portfolio=portfolio, cash=cash, stock_value=stock_value)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        if request.form.get("symbol") == "":
            return apology("No ticker inputted", 400)

        if request.form.get("shares") == "" or float(request.form.get("shares"))<= 0:
            return apology("Number of shares must be a positive number", 400)


        quote = lookup(request.form.get("symbol"))

        if not quote:
            return apology("Ticker is invalid", 400)

        cost = float(request.form.get("shares")) * quote["price"]

        cash = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        if cash[0]["cash"] < cost:
            return apology("Not enough cash", 400)

        else:
            db.execute("INSERT INTO trades (id, symbol, shares, price) VALUES(?, ?, ?, ?)",
                       session["user_id"], quote['symbol'], float(request.form.get("shares")), quote['price'])
            cash = cash[0]["cash"]
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - cost, session["user_id"])
            flash('Bought!')
            return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    portfolio = db.execute("SELECT id, symbol, shares, price, transacted  FROM trades WHERE id = ? ORDER BY transacted", session["user_id"])
    """Show history of transactions"""
    return render_template("history.html", portfolio=portfolio)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("Ticker does not exist", 400)
        return render_template("quote.html", quote= quote["symbol"] + " is " + usd(quote["price"]))

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        """Register user"""

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) == 1:
            return apology("username already exists", 400)

        if not request.form.get("username"):
            return apology("must provide username", 400)

        if not request.form.get("password"):
            return apology("must provide password", 400)

        if not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Password and confirmation must match", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) == 1:
            return apology("username already exist", 400)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password"), method='pbkdf2', salt_length=16))

        return redirect("/")
    else:
        return render_template("register.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    portfolio = db.execute("SELECT id, symbol, SUM(shares) FROM trades WHERE id = ? GROUP BY symbol HAVING SUM(shares) > 0 ORDER BY price DESC", session["user_id"])
    if request.method == "POST":
        request.form.get("symbol")
        request.form.get("shares")

        # Ensure symbol is not blank
        if request.form.get("symbol") == "":
            return apology("No ticker inputted", 400)
        if request.form.get("shares") == "":
            return apology("Number of shares must be a positive number", 400)

        quote = lookup(request.form.get("symbol"))

        if not quote:
            return apology("Ticker does not exist", 400)


        portfolio = db.execute("SELECT id, symbol, SUM(shares) FROM trades WHERE id = ? AND symbol = ? GROUP BY symbol HAVING SUM(shares)>0 ", session["user_id"], quote['symbol'])

        cash = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])


        if portfolio[0]["SUM(shares)"] < float(request.form.get("shares")):
            return apology("Too many shares being sold", 400)
        else:
            currentprice = quote['price'] * float(request.form.get("shares"))
            cash = cash[0]["cash"]
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash + currentprice, session["user_id"])
            db.execute("INSERT INTO trades (id, symbol, shares, price) VALUES(?, ?, ?, ?)", session["user_id"], quote['symbol'], -float(request.form.get("shares")), quote['price'])
            flash('Sold!')
        return redirect("/")
    else:
        return render_template("sell.html", portfolio=portfolio)

