import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
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
    # Obtener el ID del usuario
    user_id = session["user_id"]

    # Consultar las acciones del usuario
    rows = db.execute("SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0", user_id)

    # Crear una lista para almacenar la información de las acciones
    holdings = []
    total_value = 0

    # Iterar sobre las acciones del usuario
    for row in rows:
        symbol = row["symbol"]
        shares = row["total_shares"]

        # Obtener el precio actual de la acción
        stock = lookup(symbol)
        if not stock:
            return apology("Could not retrieve stock information")

        price = stock["price"]
        total = shares * price

        # Agregar la información a la lista de holdings
        holdings.append({
            "symbol": symbol,
            "shares": shares,
            "price": price,
            "total": total
        })

        # Sumar al valor total
        total_value += total

    # Obtener el saldo de efectivo del usuario
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    # Calcular el total general
    grand_total = total_value + cash

    # Renderizar la plantilla index.html con la información de las acciones y el saldo de efectivo
    return render_template("index.html", holdings=holdings, cash=cash, grand_total=grand_total)



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol")

        stock = lookup(symbol)
        if not stock:
            return apology("Invalid symbol")

        try:
            shares = int(request.form.get("shares"))  # Cambiar a int para evitar fracciones
            if shares <= 0:
                return apology("must provide positive number of shares")
        except ValueError:
            return apology("must provide a valid number of shares")

        # Consultar el efectivo del usuario
        user_id = session["user_id"]
        rows = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = rows[0]["cash"]

        # Calcular el costo total
        total_cost = shares * stock["price"]

        if cash < total_cost:
            return apology("can't afford")

        # Realizar compra
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)", user_id, symbol, shares, stock["price"])
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, user_id)

        return redirect("/")

    return render_template("buy.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions = db.execute("SELECT symbol, shares, price, timestamp FROM transactions WHERE user_id = ? ORDER BY timestamp DESC", user_id)
    return render_template("history.html", transactions=transactions)


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
        symbol = request.form.get("symbol")
        stock = lookup(symbol)
        if stock:
            return render_template("quoted.html",
                                   symbol=stock["symbol"],
                                   price=stock["price"],
                                   change=stock["change"],
                                   companyName=stock["companyName"],
                                   marketCap=stock["marketCap"],
                                   peRatio=stock["peRatio"],
                                   week52High=stock["week52High"],
                                   week52Low=stock["week52Low"])
        else:
            return apology("Invalid symbol")
    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        exist_username = db.execute("SELECT * FROM users WHERE username = ?", username)

        if not username or (len(exist_username) != 0):
            return apology("Username already exists or is empty")
        else:
            password = request.form.get("password")
            confirmation = request.form.get("confirmation")

            if not password or (password != confirmation):
                return apology("Passwords do not match or are empty")

            else:
                password_hash = generate_password_hash(password)
                db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, password_hash)
                return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol")

        try:
            shares = int(request.form.get("shares"))  # Cambiar a int para evitar fracciones
            if shares <= 0:
                return apology("must provide positive number of shares")
        except ValueError:
            return apology("must provide a valid number of shares")

        user_id = session["user_id"]

        # Verificar si el usuario posee suficientes acciones
        rows = db.execute("SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = ? AND symbol = ?", user_id, symbol)
        total_shares = rows[0]["total_shares"]

        if total_shares is None or total_shares < shares:
            return apology("not enough shares")

        # Calcular el valor de las acciones vendidas
        stock = lookup(symbol)
        total_value = shares * stock["price"]

        # Registrar la venta como una transacción negativa
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)", user_id, symbol, -shares, stock["price"])

        # Actualizar el saldo de efectivo del usuario
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_value, user_id)

        return redirect("/")

    else:
        user_id = session["user_id"]
        # Agrupar símbolos y sumar acciones para evitar duplicados
        symbols = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", user_id)
        return render_template("sell.html", symbols=[row["symbol"] for row in symbols])


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Add additional cash to the user's account"""
    user_id = session["user_id"]

    if request.method == "POST":
        # Obtener la cantidad de efectivo que el usuario quiere agregar
        try:
            amount = float(request.form.get("amount"))
            if amount <= 0:
                return apology("must provide a positive amount")
        except ValueError:
            return apology("must provide a valid amount")

        # Actualizar el saldo del usuario
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", amount, user_id)

        # Redirigir a la página principal
        return redirect("/")

    # Obtener el saldo de efectivo actual del usuario
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    return render_template("add_cash.html", cash=cash)

@app.route("/withdraw_cash", methods=["GET", "POST"])
@login_required
def withdraw_cash():
    """Withdraw cash from the user's account"""
    user_id = session["user_id"]

    if request.method == "POST":
        # Obtener la cantidad de efectivo que el usuario quiere retirar
        try:
            amount = round(float(request.form.get("amount")), 2)
            if amount <= 0:
                return apology("must provide a positive amount")
        except ValueError:
            return apology("must provide a valid amount")

        # Obtener el saldo de efectivo actual del usuario
        rows = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = round(rows[0]["cash"], 2)

        # Verificar si el usuario tiene suficiente efectivo para retirar
        if amount > cash:
            return apology("amount exceeds available cash")
        else:
            # Actualizar el saldo del usuario, evitando valores negativos
            new_cash = round(cash - amount, 2)
            if new_cash < 0:
                new_cash = 0.00

            db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, user_id)

        # Redirigir a la página principal
        return redirect("/")

    # Obtener el saldo de efectivo actual del usuario
    cash = round(db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"], 2)

    return render_template("withdraw_cash.html", cash=cash)


@app.route("/symbol_info", methods=["GET", "POST"])
@login_required
def symbol_info():
    """Retrieve information and display a TradingView chart for a given symbol."""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()

        # Verificar si el símbolo fue ingresado
        if not symbol:
            return apology("must provide a symbol")

        # Obtener la información de la acción
        stock = lookup(symbol)

        if not stock:
            return apology("invalid symbol")

        # Renderizar la plantilla con la información de la acción y el gráfico
        return render_template("symbol_info.html", stock=stock)

    return render_template("symbol_info.html")

@app.route("/delete_history", methods=["POST"])
@login_required
def delete_history():
    """Delete user's transaction history"""
    user_id = session["user_id"]

    # Eliminar el historial de transacciones del usuario
    db.execute("DELETE FROM transactions WHERE user_id = ?", user_id)

    # Redirigir al historial de transacciones
    return redirect("/history")
