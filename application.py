import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from aero import alpha_inv_analysis, alpha_visc_analysis, cl_inv_analysis, cl_visc_analysis
# Configure application
app = Flask(__name__)
app.debug = True

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data.db")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Shows saved analyses"""
    # User reached route via POST
    if request.method == "POST":
        analysis_id = request.form.get("analysis_id")
        db.execute("UPDATE analyses SET favorites = 1 WHERE analysis_id = ?", analysis_id)
        data = db.execute("SELECT * FROM analyses WHERE id = ? AND favorites = 1", session["user_id"])
        return render_template("index.html", data=data)
    # User reached route via GET
    else:
        data = db.execute("SELECT * FROM analyses WHERE id = ? AND favorites = 1", session["user_id"])
        return render_template("index.html", data=data)


    


@app.route("/history")
@login_required
def history():
    """Shows history of analyses"""
    data = db.execute("SELECT * FROM analyses WHERE id = ?", session["user_id"])
    return render_template("history.html", data=data)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)
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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via GET
    if request.method == "GET":
        return render_template("register.html")
    # User reached route via POST
    else:
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Ensures username does not already exist
        if len(rows) != 0:
            return apology("username already exists", 400)
        # Ensures password or confirmation not blank
        if not request.form.get("password") or not request.form.get("confirmation"):
            return apology("password or confirmation cannot be blank", 400)
        # Ensures password and confirmation match
        if not request.form.get("password") == request.form.get("confirmation"):
            return apology("password and confirmation must match", 400)
        # Inserts user into database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
            request.form.get("username"), generate_password_hash(request.form.get("password")))
        # Remembers user
        rows = db.execute("SELECT id FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = rows[0]["id"]
        x = session["user_id"]
        os.mkdir(f"./static/plots/{x}")
        # Redirects user to home page
        return redirect("/")


@app.route("/analyze", methods=["GET", "POST"])
@login_required
def analyze():
    """Analyzes airfoil"""
    # User reached route via GET
    if request.method == "GET":
        return render_template("analyze.html")
    # User reached route via POST
    else:
        # Collects airfoil and variable data
        airfoil = str(request.form.get("airfoil"))
        variable = request.form.get("variable")
        method = request.form.get("method")
        max_iter = int(float(request.form.get("max_iter")))
        # Deals with case where user selected alpha
        if variable == "alpha":
            alpha_i = float(request.form.get("alpha_i"))
            alpha_f = float(request.form.get("alpha_f"))
            alpha_step = float(request.form.get("alpha_step"))
            # Deals with inviscid analysis
            if method == "inv":
                alpha_inv_analysis(airfoil, alpha_i, alpha_f, alpha_step, max_iter, session["user_id"])
                # Adds analysis to table
                analysis_id = db.execute("INSERT INTO analyses (id, airfoil, method, variable, start, end, step, max_iter) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    session["user_id"], airfoil, "Inviscid", "Angle of Attack", alpha_i, alpha_f, alpha_step, max_iter)
                data = db.execute("SELECT * FROM analyses WHERE analysis_id = ?", analysis_id)
                return render_template("analysis.html", data=data)
            # Deals with viscous analysis
            elif method == "visc":
                re = float(request.form.get("re"))
                mach = float(request.form.get("mach"))
                alpha_visc_analysis(airfoil, alpha_i, alpha_f, alpha_step, re, mach, max_iter, session["user_id"])
                # Adds analysis to table
                analysis_id = db.execute("INSERT INTO analyses (id, airfoil, method, variable, re, mach, start, end, step, max_iter) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    session["user_id"], airfoil, "Viscous", "Angle of Attack", re, mach, alpha_i, alpha_f, alpha_step, max_iter)
                data = db.execute("SELECT * FROM analyses WHERE analysis_id = ?", analysis_id)
                return render_template("analysis.html", data=data)
        # Deals with case where user selected cl
        if variable == "cl":
            cl_i = float(request.form.get("cl_i"))
            cl_f = float(request.form.get("cl_f"))
            cl_step = float(request.form.get("cl_step"))
            # Deals with inviscid analysis
            if method == "inv":
                cl_inv_analysis(airfoil, cl_i, cl_f, cl_step, max_iter, session["user_id"])
                analysis_id = db.execute("INSERT INTO analyses (id, airfoil, method, variable, start, end, step, max_iter) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    session["user_id"], airfoil, "Inviscid", "Coefficient of Lift", cl_i, cl_f, cl_step, max_iter)
                data = db.execute("SELECT * FROM analyses WHERE analysis_id = ?", analysis_id)
                return render_template("analysis.html", data=data)
            elif method == "visc":
                re = float(request.form.get("re"))
                mach = float(request.form.get("mach"))
                cl_visc_analysis(airfoil, cl_i, cl_f, cl_step, re, mach, max_iter, session["user_id"])
                analysis_id = db.execute("INSERT INTO analyses (id, airfoil, method, variable, re, mach, start, end, step, max_iter) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    session["user_id"], airfoil, "Viscous", "Coefficient of Lift", re, mach, cl_i, cl_f, cl_step, max_iter)
                data = db.execute("SELECT * FROM analyses WHERE analysis_id = ?", analysis_id)
                return render_template("analysis.html", data=data)

        
    
                






def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

