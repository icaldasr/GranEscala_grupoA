#my_app.py

import os
from flask import Flask, render_template, request, redirect, session, g, url_for, flash, jsonify, make_response, send_from_directory
from clases.Sistema import Sistema
import secrets
from datetime import datetime,date
import time
import requests

import json

from json import loads

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
        

@app.route("/registrarDoctor", methods = ["POST", "GET"])
def registrarDoctor():
    if "user" in session:
        usuario = session["user"]
        contra = secrets.token_urlsafe(6)
        tipo_documentos = sis.tipo_documento()
        epss = sis.obtener_eps()
        espcc = sis.obtener_espc()
        ciu = sis.obtener_ciudades()
        if request.method == 'POST':
            term = request.form.get('terminos')
            if term == "on":
                nombre = request.form["nombre"]
                apellido = request.form["apellido"]
                tipodoc = request.form["TD"]
                nrodocumento = request.form["numeroDocumento"]
                eps = request.form["ideps"]
                especializacion = request.form["esp"]
                rh = request.form["RH"]
                correo = request.form["correo"]
                nacimiento = request.form["fecnac"]
                tel = request.form["tel"]
                #departamento = request.form["departamento"]
                ciudad = request.form["ciudad"]
                barrio = request.form["barrio"]
                sexo = request.form["sex"]
                ##Falta cambiar en el formulario los valores especificos de las opciones de seleccion que van en la BD 
                x = sis.agregarDoctor(tipodoc, int(nrodocumento), nombre, apellido, eps, especializacion, rh, correo, nacimiento, int(tel), ciudad, barrio, sexo, contra)
                if x == 1:
                    mensaje = '¡Doctor creado satisfactoriamente!'
                    flash(mensaje,"success")
                    sis.enviarDatosLogin(correo,contra,'Doctor')
                    ##print (nombre + " - " + apellido + " - "+ tipodoc + " - " + nrodocumento +" - "+ ideps + " - " + nacimiento + " - " + rh+" - " + correo  + " - " + sexo + " - " +term)
                    return redirect(url_for("admin"))
                elif x == 2:
                    mensaje = '¡Un usuario con este número de documento ya existe! No puedes agregar una persona con dos cuentas en el sistema.'
                    flash(mensaje,"error")
                elif x == 3: 
                    mensaje = '¡Un usuario con este correo ya existe! Usa otro correo. '
                    flash(mensaje,"error")
            else:
                mensaje = '¡Debes aceptar los términos y condiciones para continuar!'
                flash(mensaje,"error")
        return render_template("registrardoctor.html", t_d = tipo_documentos, ep=epss, esp=espcc, ci = ciu)
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
            if term != None:
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
                nombreCompleto = '{} {}'.format(nombre,apellido)
                #print(nacimiento)
                #print("NombreCompleto",nombreCompleto)
                agregar = sis.agregarPaciente(int(nrodocumento),nombreCompleto,nacimiento,eCivil,int(telefono),sexo)
                if agregar == 1:
                    mensaje = '¡Paciente creado satisfactoriamente!'
                    flash(mensaje,"success")
                #sis.agregarPaciente()
                else:
                    mensaje = '¡El paciente no ha sido creado! Intentélo nuevamente'
                    flash(mensaje,"error")
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
        tipo_documentos = sis.tipo_documento()
        #epss = sis.obtener_eps()
        #espcc = sis.obtener_espc()
        ciu = sis.obtener_ciudades()
        if request.method == 'POST':
            term = request.form.get('terminos')
            if term == "on":
                nombre = request.form["nombre"]
                apellido = request.form["apellido"]
                tipoDoc = request.form["tipoDoc"]
                nrodocumento = request.form["numeroDocumento"]
                #rh = request.form["RH"]
                correoE = request.form["correoE"]
                #nacimiento = request.form["fNacimiento"]
                telefono = request.form["tel"]
                #eCivil = request.form["EC"]
                departamento = request.form["departamento"]
                ciudad = request.form["ciudad"]
                barrio = request.form["barrio"]
                sexo = request.form["sexoAdmin"]
                
                x = sis.agregarAdmin(nrodocumento, nombre, apellido, contra,correoE,tipoDoc,telefono)

                if x == 1:
                    mensaje = '¡Administrador creado satisfactoriamente!'
                    flash(mensaje,"success")
                    sis.enviarDatosLogin(correoE,contra,'Administrador')
                    ##print (nombre + " - " + apellido + " - "+ tipodoc + " - " + nrodocumento +" - "+ ideps + " - " + nacimiento + " - " + rh+" - " + correo  + " - " + sexo + " - " +term)
                    return redirect(url_for("admin"))
                elif x == 2:
                    mensaje = '¡Un usuario con este número de documento ya existe! No puedes agregar una persona con dos cuentas en el sistema.'
                    flash(mensaje,"error")
                elif x == 0: 
                    mensaje = '¡Un usuario con este correo ya existe! Usa otro correo. '
                    flash(mensaje,"error")

            else:
                mensaje = '¡Debes aceptar los términos y condiciones para continuar!'
                flash(mensaje,"error")
        return render_template("registraradmin.html", t_d = tipo_documentos, ci = ciu)
    else: 
        message = '¡Primero debes iniciar sesión!'
        flash(message,"error")
        return redirect(url_for("login"))

@app.route("/solicitudes", methods = ["POST","GET"])
def solicitudes():
    if "user" in session:
        usuario = session["user"]
        solicitudes = sis.mostrarSolicitudes()
        return render_template("solicitudes.html",solicitudes=solicitudes)
    else: 
        message = '¡Primero debes iniciar sesión!'
        flash(message,"error")
        return redirect(url_for("login"))

@app.route("/ActualizarSolicitud",methods =["POST","GET"])
def actualizarSolicitudesFuncion():
    if "user" in session:
        usuario = session["user"]
        if request.method == 'POST':
            solicitudes = sis.mostrarSolicitudes()
            req = request.form['json_string']
            data = loads(req)
            #print(data['idSolicitud'])
            #print(data)
            solicitudesActualizadas = sis.obtenerSolicitudesActualizadas(data)
            #print(solicitudesActualizadas)

            mensaje = 1

            for i in solicitudesActualizadas:
                idSolicitud = i[0]
                estadoActual = i[1]
                justificacion = i[2]
                cambio = i[4]

                if cambio == False:
                    #if estadoActual == 'Rechazado':
                     #   print("NSTADO RECHAZADO",idSolicitud)
                    #else:
                     #   print("CAMBIO A ESTADO RECHAZADO",idSolicitud)
                        #mensaje = 1
                    sis.actualizarSolicitud(idSolicitud,estadoActual,justificacion)
                else:
                    #print("TRUE",idSolicitud)
                    if justificacion == 'None':
                        #print("NO SE ACTUALIZA")
                        mensaje = 0
                        #flash("NO SE ACTUALIZA","error")
                    else:
                        #print("SI SE ACTUALIZA")
                        sis.actualizarSolicitud(idSolicitud,estadoActual,justificacion)
                        #mensaje = 1

            if mensaje == 0:
                print("MENSAJE NO ACTUALIZA")
                return ('No Funciona',200)

            else:
                print("MENSAJE SI ACTUALIZA")
                flash('Solicitudes actualizadas',"success")
                sis.actualizarSolicitud(idSolicitud,estadoActual,justificacion)
                return ('Funciona',200)

            return render_template("solicitudes.html",solicitudes=solicitudes)
    else: 
        message = '¡Primero debes iniciar sesión!'
        flash(message,"error")
        return redirect(url_for("login"))

@app.route("/guardarSolicitud",methods = ["POST", "GET"])
def guardarSolicitud():
    if "user" in session:
        usuario = session["user"]
        if request.method == 'POST':
            print("ACTUALIZADO")
            solicitudes = sis.mostrarSolicitudes()
            print(solicitudes)
        return redirect(url_for("admin"))
            #return render_template("solicitudes.html",solicitudes=solicitudes)

    else: 
        message = '¡Primero debes iniciar sesión!'
        flash(message,"error")
        return redirect(url_for("login"))

@app.route("/doctor", methods = ["POST", "GET"])
def doctor():
    if "user" in session:
        usuario = session["user"]
        doc = sis.cargarDoctor(session["user"])
        return render_template("doctor.html",  nombre=doc.getNombre(), correo= usuario, apellido= doc.getApellido())
    else:
        message = '¡Primero debes iniciar sesión!'
        flash(message,"error")
        return redirect(url_for("login"))

@app.route("/citaPaciente", methods = ['POST', 'GET'])
def citaPaciente():
    if "user" in session:
        doc = sis.cargarDoctor(session["user"])
        hora = time.localtime()
        horaActual = time.strftime("%H:%M:%S", hora)
        fechaAct = date.today() #https://www.programiz.com/python-programming/datetime/current-datetime
        idDoctor = doc.getNumeroDoc()
        idPaciente = 333333
        #recibir = sis.recibirTokenHCCORE()
        #print(fechaAct)
        #print(current_time)
        #print("timestamp =", timestamp)
        #print("token: ",recibir)
        if request.method == 'POST':
            #fecha = request.form[""]
            motivo =request.form["motivo"]
            observaciones = request.form["observaciones"]
            conciencia = request.form["conciencia"]
            lenguaje = request.form["lenguaje"]
            auditivo = request.form["auditivo"]
            agudezaVisual = request.form["agudeza"]
            peso = request.form["peso"]
            estatura = request.form["estatura"]
            presion = request.form["presion"]
            facie = request.form["facie"]
            edad = request.form["edad"]
            temperatura = request.form["temperatura"]
            alimentacion = request.form["alimentacion"]
            apetito = request.form["apetito"]
            sed = request.form["sed"]
            diuresis = request.form["diuresis"]
            catarsis = request.form["catarsis"]
            sueno = request.form["sueño"]
            relaciones = request.form["Relaciones"]
            alcohol = request.form["alcohol"]
            tabaco = request.form["Tabaco"]
            drogas = request.form["drogas"]
            medicacion = request.form["medicacion"]
            resultados = request.form["resultados"]
            anexos = request.form["anexos"]
            lactancia = request.form["lactancia"]
            iniciacion = request.form["iniciacion"]
            gineco = request.form["gineco"]
            menarca = request.form["menarca"]
            embarazos = request.form["Embarazos"]
            partos = request.form["partos"]
            abortos = request.form["abortos"]
            gramaje = request.form["gramaje"]
            resumen = request.form["resumen"]
            diagnostico = request.form["diagnostico"]

            #Medicamentos
            cb1 = request.form.get("cbox1")
            if cb1 != None:
                print(cb1)
                sis.insertarSolicitud(cb1,"Aprobado",idDoctor,idPaciente)
            cb2 = request.form.get("cbox2") 
            if cb2 != None:
                print(cb2)
                sis.insertarSolicitud(cb2,"Aprobado",idDoctor,idPaciente)
            cb3 = request.form.get("cbox3") 
            if cb3 != None:
                print(cb3)
                sis.insertarSolicitud(cb3,"Pendiente",idDoctor,idPaciente)
            cb4 = request.form.get("cbox4") 
            if cb4 != None:
                print(cb4)
                sis.insertarSolicitud(cb4,"Pendiente",idDoctor,idPaciente)
            cb5 = request.form.get("cbox5") 
            if cb5 != None:
                print(cb5)
                sis.insertarSolicitud(cb5,"Pendiente",idDoctor,idPaciente)

            inidicacionesMedicamentos = request.form["InidicacionesMedicamentos"]
            incapacidad = request.form["incapacidad"]
            if incapacidad != '':
                sis.insertarSolicitud(incapacidad,"Pendiente",idDoctor,idPaciente)

            #Remisiones
            cb6 = request.form.get("cbox6")
            if cb6 != None:
                print(cb6)
                sis.insertarSolicitud(cb6,"Pendiente",idDoctor,idPaciente)
            cb7 = request.form.get("cbox7") 
            if cb7 != None:
                print(cb7)
                sis.insertarSolicitud(cb7,"Pendiente",idDoctor,idPaciente)
            cb8 = request.form.get("cbox8") 
            if cb8 != None:
                print(cb8)
                sis.insertarSolicitud(cb8,"Pendiente",idDoctor,idPaciente)
            cb9 = request.form.get("cbox9") 
            if cb9 != None:
                print(cb9)
                sis.insertarSolicitud(cb9,"Pendiente",idDoctor,idPaciente)
            cb10 = request.form.get("cbox10") 
            if cb10 != None:
                print(cb10)
                sis.insertarSolicitud(cb10,"Pendiente",idDoctor,idPaciente)

            #Examenes
            cb11 = request.form.get("cbox11")
            if cb11 != None:
                print(cb11)
                sis.insertarSolicitud(cb11,"Pendiente",idDoctor,idPaciente)
            cb12 = request.form.get("cbox12") 
            if cb12 != None:
                print(cb12)
                sis.insertarSolicitud(cb12,"Pendiente",idDoctor,idPaciente)
            cb13 = request.form.get("cbox13") 
            if cb13 != None:
                print(cb13)
                sis.insertarSolicitud(cb13,"Pendiente",idDoctor,idPaciente)
            cb14 = request.form.get("cbox14") 
            if cb14 != None:
                print(cb14)
                sis.insertarSolicitud(cb14,"Pendiente",idDoctor,idPaciente)
            cb15 = request.form.get("cbox15") 
            if cb15 != None:
                print(cb15)
                sis.insertarSolicitud(cb15,"Pendiente",idDoctor,idPaciente)

            #Tratamientos
            cb16 = request.form.get("cbox16")
            if cb16 != None:
                print(cb16)
                sis.insertarSolicitud(cb16,"Pendiente",idDoctor,idPaciente)
            cb17 = request.form.get("cbox17") 
            if cb17 != None:
                print(cb17)
                sis.insertarSolicitud(cb17,"Pendiente",idDoctor,idPaciente)
            cb18 = request.form.get("cbox18") 
            if cb18 != None:
                print(cb13)
                sis.insertarSolicitud(cb18,"Pendiente",idDoctor,idPaciente)
            cb19 = request.form.get("cbox19") 
            if cb19 != None:
                print(cb19)
                sis.insertarSolicitud(cb19,"Pendiente",idDoctor,idPaciente)
            cb20 = request.form.get("cbox20") 
            if cb20 != None:
                print(cb20)
                sis.insertarSolicitud(cb20,"Pendiente",idDoctor,idPaciente)

            mensaje = '¡Cita cargada satisfactoriamente!'
            flash(mensaje,"success")
            
            print(partos)
            return redirect(url_for("doctor"))
        return render_template("cita.html")
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
#        return "JSON recibido"
    
 #   else:
    flash("No se ha recibido la Historia Clínica del paciente","error")

    return redirect(url_for("doctor"))

@app.route("/mostrarHC", methods = ['POST', 'GET'])
def json():
    if "user" in session:
        if request.form.get('DNI') != None:
            dni = request.form.get('DNI')
            x = sis.getHCPaciente(dni)
            if(x[0] == 3):
                flash("Esta historia clínica no existe", "error")
                return redirect(url_for("buscar"))
            elif (x[0] == 1):
                #pdfname = sis.JSONtoPDF(x[1])
                print (str(x[1]))
                return redirect("mostrarHC/{}".format(str(x[1])))  #"<h1>El dni es: " + str(dni) + "y el mensaje de retorno es: "+ str(x)+ " </h1>"
            else:
                flash("¡Ha ocurrido un error vuelva a intentarlo!", "error")
                return redirect(url_for("buscar"))
            #return redirect(url_for("mostrarpdf"))
        
        else:
            flash("¡Debe introducir un número de documento de un paciente!", "error")
            return redirect(url_for('buscar'))
    
    else:
        message = '¡Primero debes iniciar sesión!'
        flash(message,"error")
        return redirect(url_for("login"))


@app.route('/mostrarHC/<dire>/<pdfname>')
def open(dire, pdfname):    
    print ("NombrePDF = {}".format(pdfname))
    return send_from_directory(directory = dire, filename=pdfname, mimetype='application/pdf')

@app.route("/logout")
def logout():
    if "user" in session:
        usuario = session["user"]
        #flash("Se cerró sesión correctamente", "info")
    session.pop("user", None)
    
    return redirect(url_for("login"))

