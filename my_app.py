#my_app.py

import os
from flask import Flask, render_template, request, redirect, session, g, url_for, flash
from clases.Sistema import Sistema
import secrets

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
        correo2 = request.form['correo2']
        print(correo)
        sis.enviarClave(correo)
        mensaje = 'Contraseña enviada al correo {}'.format(correo)
        flash(mensaje)
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
        contra = secrets.token_urlsafe(6)
        if request.method == 'POST':
            term = request.form.get('terminos')
            if term == "on":
                nombre = request.form["nombre"]
                apellido = request.form["apellido"]
                tipodoc = request.form["TD"]
                nrodocumento = request.form["numeroDocumento"]
                ideps = request.form["ideps"]
                idespecializacion = request.form["esp"]
                rh = request.form["RH"]
                correo = request.form["correo"]
                nacimiento = request.form["fecnac"]
                tel = request.form["tel"]
                departamento = request.form["departamento"]
                ciudad = request.form["ciudad"]
                barrio = request.form["barrio"]
                sexo = request.form["sex"]
                ##Falta cambiar en el formulario los valores especificos de las opciones de seleccion que van en la BD 
                #sis.agregarDoctor(int(tipodoc), int(nrodocumento), nombre, apellido, int(ideps), int(idespecializacion), rh, correo, nacimiento, int(tel), departamento, ciudad, bario, sexo)
                print (nombre + " - " + apellido + " - "+ tipodoc + " - " + nrodocumento +" - "+ ideps + " - " + nacimiento + " - " + rh+" - " + correo  + " - " + sexo + " - " +term)
                return redirect(url_for("admin"))
            
        return render_template("registrardoctor.html")
    else: 
        return "ERROR: No ha iniciado sesión"

@app.route("/registrarPaciente", methods = ["POST", "GET"])
#FALTA GUARDAR
def registrarPaciente():
    if "user" in session:
        usuario = session["user"]
        if request.method == 'POST':
            term = reques.form.get('terminos')
            if term == "on":
                nombre = request.form["nombre"]
                apellido = request.form["apellido"]
                tipodoc = request.form["TDP"]
                nrodocumento = request.form["numeroDocumento"]
                rh = request.form["RH"]
                nacimiento = request.form["fechaNacimiento"]
                eCivil = request.form["EC"]
                telefono = request.form["tel"]
                departamento = request.form["departamento"]
                ciudad = request.form["ciudad"]
                barrio = request.form["barrio"]
                sexo = request.form["sexo"]
                return redirect(url_for("admin"))

        return render_template("registrarpaciente.html")
    else: 
        return "ERROR: No ha iniciado sesión"

@app.route("/registrarAdministrador", methods = ["POST", "GET"])
def registrarAdministrador():
    if "user" in session:
        usuario = session["user"]
        contra = secrets.token_urlsafe(6)
        #print("CONTRASEÑA",contra)
        if request.method == 'POST':
            term = reques.form.get('terminos')
            if term == "on":
                nombre = request.form["nombre"]
                apellido = request.form["apellido"]
                tipodoc = request.form["TDA"]
                nrodocumento = request.form["numeroDocumento"]
                rh = request.form["RH"]
                correoE = request.form["correoE"]
                nacimiento = request.form["fNacimiento"]
                telefono = request.form["tel"]
                #eCivil = request.form["EC"]
                departamento = request.form["departamento"]
                ciudad = request.form["ciudad"]
                barrio = request.form["barrio"]
                sexo = request.form["sexo"]
                sis.agregarAdmin(nrodocumento, nombre, apellido, correoE,telefono,tipodoc,contra)
                return redirect(url_for("admin"))
            else:
                print("ERROR")
        return render_template("registraradmin.html")
    else: 
        
        return "ERROR: No ha iniciado sesión"

@app.route("/solicitudes", methods = ["POST","GET"])
def solicitudes():
    if "user" in session:
        usuario = session["user"]
        return render_template("solicitudes.html")
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