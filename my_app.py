#my_app.py

import os
from flask import Flask, render_template, request, redirect, session, g, url_for, flash
from flask_mysqldb import MySQL
from clases.Sistema import Sistema

app = Flask(__name__)
app.secret_key = "ValleDev1234"
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
            return redirect(url_for("logout"))  ##aqui se puede cambiar la conf para que cuando se cierre el navegador se mantenga la sesion iniciada
        return render_template("login.html")


@app.route("/admin", methods = ["POST", "GET"])
def admin():
    if "user" in session:
        usuario = session["user"]
        return render_template("admin.html")
    else:
        return redirect(url_for("login"))

@app.route("/Buscar", methods = ["POST", "GET"])
def buscar():
    return render_template("admin_2.html")

@app.route("/registrarDoctor", methods = ["POST", "GET"])
def registrarDoctor():
    return "Registro Doctor"##redirect(url_for("registrarMedico.html"))  ##No existe aun


@app.route("/registrarPaciente", methods = ["POST", "GET"])
def registrarPaciente():
    return "Registro Paciente"##redirect(url_for("registrarPaciente.html"))  ##No existe aun

@app.route("/registrarAdministrador", methods = ["POST", "GET"])
def registrarAdministrador():
    return redirect(url_for("registrarAdministador.html"))  ##No existe aun



@app.route("/doctor", methods = ["POST", "GET"])
def doctor():
    if "user" in session:
        usuario = session["user"]
        return f"<h1>{usuario}</h1>" ##Debe mostrar la página inicial de doctor
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    if "user" in session:
        usuario = session["user"]
        #flash("Se cerró sesión correctamente", "info")
    session.pop("user", None)
    
    return redirect(url_for("login"))