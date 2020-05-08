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
            mensaje = 'El correo o la contraseña son erroneos. ¡Vuelve a intentarlo!'
            flash(mensaje,"error")
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

        if correo != correo2:
            flash("Los correos ingresados no coinciden, intente nuevamente","error")

        else: 
            if sis.enviarClave(correo) == True:
                mensaje = 'Contraseña enviada al correo {}'.format(correo)
                flash('Contraseña enviada al correo {}'.format(correo),"success")
            else:
                mensaje = 'El correo no está registardo'
                flash("El correo ingresado no está registrado en el sistema","error")
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
        message = '¡Primero debes iniciar sesión!'
        flash(message,"error")
        return redirect(url_for("login"))
        
@app.route("/Buscar", methods = ["POST", "GET"])
def buscar():
    if "user" in session:
        usuario = session["user"]
        return render_template("admin_2.html")
    else: 
        message = '¡Primero debes iniciar sesión!'
        flash(message,"error")
        return redirect(url_for("login"))

@app.route("/registrarDoctor", methods = ["POST", "GET"])
def registrarDoctor():
    if "user" in session:
        usuario = session["user"]
        contra = secrets.token_urlsafe(6)
        tipo_documentos = sis.tipo_documento()
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
                #departamento = request.form["departamento"]
                ciudad = request.form["ciudad"]
                barrio = request.form["barrio"]
                sexo = request.form["sex"]
                ##Falta cambiar en el formulario los valores especificos de las opciones de seleccion que van en la BD 
                #sis.agregarDoctor(int(tipodoc), int(nrodocumento), nombre, apellido, int(ideps), int(idespecializacion), rh, correo, nacimiento, int(tel), departamento, ciudad, bario, sexo)
                print (nombre + " - " + apellido + " - "+ tipodoc + " - " + nrodocumento +" - "+ ideps + " - " + nacimiento + " - " + rh+" - " + correo  + " - " + sexo + " - " +term)
                mensaje = '¡Doctor creado satisfactoriamente!'
                flash(mensaje,"success")
                sis.enviarDatosLogin(correo,contra,'Doctor')
                return redirect(url_for("admin"))
            else:
                mensaje = '¡Debes aceptar los términos y condiciones para continuar!'
                flash(mensaje,"error")
        return render_template("registrardoctor.html", t_d = tipo_documentos)
    else: 
        message = '¡Primero debes iniciar sesión!'
        flash(message,"error")
        return redirect(url_for("login"))

@app.route("/registrarPaciente", methods = ["POST", "GET"])
#FALTA GUARDAR
def registrarPaciente():
    if "user" in session:
        usuario = session["user"]
        if request.method == 'POST':
            term = request.form.get('terminos')
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
                mensaje = '!Paciente creado satisfactoriamente!'
                flash(mensaje)

                return redirect(url_for("admin"))
            else:
                message = '¡Debes aceptar los términos y condiciones para continuar!'
                flash(message,"error")

        return render_template("registrarpaciente.html")
    else: 
        message = '¡Primero debes iniciar sesión!'
        flash(message,"error")
        return redirect(url_for("login"))

@app.route("/registrarAdministrador", methods = ["POST", "GET"])
def registrarAdministrador():
    if "user" in session:
        usuario = session["user"]
        contra = secrets.token_urlsafe(6)
        #print("CONTRASEÑA",contra)
        tipo_documentos = sis.tipo_documento()
        if request.method == 'POST':
            term = request.form.get('terminos')
            if term == "on":
                # nombre = request.form["nombre"]
                # apellido = request.form["apellido"]
                # tipodoc = request.form["TDA"]
                # nrodocumento = request.form["numeroDocumento"]
                # rh = request.form["RH"]
                correoE = request.form["correoE"]
                # nacimiento = request.form["fNacimiento"]
                # telefono = request.form["tel"]
                # #eCivil = request.form["EC"]
                # departamento = request.form["departamento"]
                # ciudad = request.form["ciudad"]
                # barrio = request.form["barrio"]
                # sexo = request.form["sexo"]
                #sis.agregarAdmin(nrodocumento, nombre, apellido, correoE,telefono,tipodoc,contra)
                #sis.agregarAdmin(nrodocumento, nombre, apellido, correoE,telefono,tipodoc,contra)

                mensaje = '¡Administrador creado satisfactoriamente!'
                flash(mensaje,"success")
                sis.enviarDatosLogin(correoE,contra,'Administrador')
                return redirect(url_for("admin"))
            else:
                message = '¡Debes aceptar los términos y condiciones para continuar!'
                flash(message,"error")
        return render_template("registraradmin.html",t_d = tipo_documentos)
    else: 
        message = '¡Primero debes iniciar sesión!'
        flash(message,"error")
        return redirect(url_for("login"))

@app.route("/solicitudes", methods = ["POST","GET"])
def solicitudes():
    if "user" in session:
        usuario = session["user"]
        return render_template("solicitudes.html")
    else: 
        message = '¡Primero debes iniciar sesión!'
        flash(message,"error")
        return redirect(url_for("login"))

@app.route("/doctor", methods = ["POST", "GET"])
def doctor():
    if "user" in session:
        usuario = session["user"]
        return f"<h1>{usuario}</h1>" ##Debe mostrar la página inicial de doctor
    else:
        message = '¡Primero debes iniciar sesión!'
        flash(message,"error")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    if "user" in session:
        usuario = session["user"]
        #flash("Se cerró sesión correctamente", "info")
    session.pop("user", None)
    
    return redirect(url_for("login"))




if __name__ == "__main__":
    app.run(debug=True)