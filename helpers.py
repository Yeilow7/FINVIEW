import csv
import datetime
import pytz
import requests
import urllib
import uuid

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def lookup(symbol):
    """Look up quote for symbol."""

    # Preparar la solicitud a la API
    symbol = symbol.upper()
    end = datetime.datetime.now(pytz.timezone("US/Eastern"))
    start = end - datetime.timedelta(days=7)

    # API de Yahoo Finance
    url = (
        f"https://query1.finance.yahoo.com/v7/finance/download/{urllib.parse.quote_plus(symbol)}"
        f"?period1={int(start.timestamp())}"
        f"&period2={int(end.timestamp())}"
        f"&interval=1d&events=history&includeAdjustedClose=true"
    )

    # Consulta a la API
    try:
        response = requests.get(
            url,
            cookies={"session": str(uuid.uuid4())},
            headers={"Accept": "*/*", "User-Agent": request.headers.get("User-Agent")},
        )
        response.raise_for_status()

        # Analizar el CSV devuelto por la API
        quotes = list(csv.DictReader(response.content.decode("utf-8").splitlines()))
        latest = quotes[-1]

        # Datos que podemos obtener de Yahoo Finance
        price = round(float(latest["Adj Close"]), 2)
        change = price - round(float(latest["Open"]), 2)  # Diferencia entre el precio de apertura y el precio actual
        companyName = "Company Name Placeholder"  # Placeholder para el nombre de la empresa
        market_cap = 1234567890  # Ejemplo de capitalización de mercado
        pe_ratio = 25.67  # Ejemplo de relación P/E
        week52_high = round(float(latest["High"]), 2) + 10  # Ejemplo de máximo de 52 semanas
        week52_low = round(float(latest["Low"]), 2) - 10  # Ejemplo de mínimo de 52 semanas

        return {
            "symbol": symbol,
            "price": price,
            "change": round(change, 2),
            "companyName": companyName,
            "marketCap": market_cap,
            "peRatio": pe_ratio,
            "week52High": week52_high,
            "week52Low": week52_low
        }
    except (KeyError, IndexError, requests.RequestException, ValueError) as e:
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"
