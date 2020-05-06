#my_app.py

import os
from flask import Flask, render_template, request, redirect, session, g, url_for, flash
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

@app.route('/recuperar', methods = ['POST', 'GET'])
def cambioContrasena():
    if request.method == 'POST':
        correo = request.form['correo1']
        print(correo)
        sis.enviarClave(correo)
    return redirect(url_for("login"))
    #return render_template("login.html")

@app.route("/admin", methods = ["POST", "GET"])
def admin():
    if "user" in session:
        usuario = session["user"]
        #ad es objeto Administrador
        ad = sis.cargarAdmin(session["user"])   #carga el usuario en clase Administrador
        if(ad != None):
            return render_template("admin.html", nombre=ad.getNombre(), correo= usuario)
        else:
            return render_template("admin.html", nombre="UnNombre", correo= usuario)
    else:
        return redirect(url_for("login"))

@app.route("/Buscar", methods = ["POST", "GET"])
def buscar():
    if "user" in session:
        usuario = session["user"]
        return render_template("admin_2.html")
    else: 
        return "ERROR: No ha iniciado sesión"

@app.route("/registrarDoctor", methods = ["POST", "GET"])
def registrarDoctor():
    if "user" in session:
        usuario = session["user"]
        return render_template("registrardoctor.html")
    else: 
        return "ERROR: No ha iniciado sesión"


@app.route("/registrarPaciente", methods = ["POST", "GET"])
def registrarPaciente():
    if "user" in session:
        usuario = session["user"]
        return render_template("registrarpaciente.html")
    else: 
        return "ERROR: No ha iniciado sesión"

@app.route("/registrarAdministrador", methods = ["POST", "GET"])
def registrarAdministrador():
    if "user" in session:
        usuario = session["user"]
        return render_template("registraradmin.html")
    else: 
        return "ERROR: No ha iniciado sesión"

@app.route("/solicitudes", methods = ["POST","GET"])
def solicitudes():
    if "user" in session:
        usuario = session["user"]
        return "Hola amigo Otoya" #render_template("solicitudes.html")
    else: 
        return "ERROR: No ha iniciado sesión"



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