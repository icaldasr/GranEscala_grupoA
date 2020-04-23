#my_app.py

import os
from flask import Flask, render_template, request, redirect, session, g, url_for, flash
from flask_mysqldb import MySQL
from clases.Sistema import Sistema

app = Flask(__name__)
app.secret_key = "ValleDev1234"
#app.config['MYSQL_USER'] = '203256'
#app.config['MYSQL_PASSWORD'] = 'juancamilo99'
#app.config['MYSQL_HOST'] = 'mysql-historiasclinicas.alwaysdata.net'
#app.config['MYSQL_DB'] = 'historiasclinicas_bd'
#mysql = MySQL(app)
sis = Sistema()

@app.route("/", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        #session.pop('user', None)
        nomusuario = request.form["uname"]
        clave = request.form["psw"]
        session["user"] = nomusuario
        if sis.login(nomusuario,clave) == 1:
            session['user'] = nomusuario 
            return redirect(url_for("admin"))
        elif sis.login(nomusuario,clave) == 2:
            session['user'] = nomusuario 
            return redirect(url_for("doctor"))
        else:
            return render_template("login.html")
    else:
        if "user" in session:
            return redirect(url_for("logout"))
        return render_template("login.html")


@app.route("/admin", methods = ["POST", "GET"])
def admin():
    if "user" in session:
        usuario = session["user"]
        return f"<h1>{usuario}</h1>"
    else:
        return redirect(url_for("login"))


@app.route("/doctor", methods = ["POST", "GET"])
def doctor():
    if "user" in session:
        usuario = session["user"]
        return f"<h1>{usuario}</h1>"
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))