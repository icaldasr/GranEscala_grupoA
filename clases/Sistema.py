#Sistema.py
#Autor: Luis Miguel Oviedo
#smtp lib para envío de mensajes en recuperacion de la clave de ingreso
import smtplib
import requests
import json
from fpdf import fpdf
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
##dentro del proyecto
from clases.Gestor import Gestor
from clases.SolicitudM import SolicitudM
from clases.HistoriaClinica import HistoriaClinica
from clases.Administrador import Administrador
from clases.Doctor import Doctor
import secrets
from email.header import Header
from email.utils import formataddr



class Sistema():
    instance = None
    @staticmethod
    def getInstance():
        if not Sistema.instance:
            Sistema.__init__()
        return Sistema.instance

    def __init__(self):
        if Sistema.instance != None:
            raise Exception("Esta es una instancia unica")
        else:
            Sistema.instance = self
            self.pacientes= []
            self.administradores = []
            self.doctores = []
            self.citas = []
            self.solicitudes = []
            self.dataBase = Gestor()
            self.ensesion = []
            


    def login(self, nomusr, psw):
        ##verificar con base de datos si existe 
        if (nomusr != None) and (psw != None):
            rol = None
            tipoDoc = None
            doc = None
            temp = self.dataBase.getLoginInfo()  ## join entre admins(1) y doctores(2)
            if temp != None:
                for i in temp:
                    if i[1] == nomusr and i[2] == psw:  #i[0] nombre i[1] correo i[2] psw i[3] tipousr
                        rol = i[3]
                        break
                
                if rol == "administrador":
                    for x in self.administradores:
                        if x.getUsuario() == nomusr and x.getClave() == psw:
                            self.ensesion.append(x)
                    return 1
                elif rol == "medico": 
                    for x in self.doctores:
                        if x.getUsuario() == nomusr and x.getClave() == psw:
                            self.ensesion.append(x)
                    return 2
                else: 
                    return -1
            else:
                return -1
        else:
            return -1

    def agregarDoctor(self, tipodoc, nrodocumento, nombre, apellido, ideps, idespecializacion, rh, correo, nacimiento, tel, ciudad, barrio, sexo, contra):
        x = self.dataBase.insertarDoctor(tipodoc, nrodocumento, nombre, apellido, ideps, idespecializacion, rh, correo, nacimiento, tel, ciudad, barrio, sexo, contra)
        return x

    def agregarAdmin(self,nrodocumento, nombre, apellido, contra,correo,tipoDoc,telefono):
        y = self.dataBase.insertarAdministrador(nrodocumento, nombre, apellido, contra,correo,tipoDoc,telefono)
        return y
    
    def posDoctor(self, tipodoc, numdoc):
        cont = 0
        found = False
        for i in self.doctores:
            if i.getTipoDoc() == tipodoc  and i.getNumeroDoc() == numdoc:
                found = True
                break
            cont += 1

        if found == True:
            return cont
        else: 
            return -1


    def darDeBajaDoctor(self, tipoDoc, numDoc):
        x = self.posDoctor(tipoDoc, numDoc)
        if x < 0:
            print("El médico no existe")
        else: 
            self.doctores.pop(x)
            print("Procedimiento de remover médico exitoso")

    def actualizarCitaBD(Cita):
        #llamargestor db y actualizar con esa cita
        return 0

    def actualizarPacienteBD(Paciente):
        #llamargestor db y actualizar con esa cita
        return 0
            
    def nuevoIdCita(self):
        return self.dataBase.nuevoIdCita()

    def nuevaCita(self, cit):
        self.citas.append(cit)

    def crearSolicitudM(self, med, pac, doc):
        x = self.database.nuevoIdSolicitudM()
        self.solicitudes.append(SolicitudM(x, med, pac, doc))

    def getSolicitudM(self):
        for i in self.solicitudes:
            if i.getEstado() == "esperando":
                return i
        return None

    def enviarClave(self, correo):
        msg = MIMEMultipart()
        
        existe = self.dataBase.buscarCorreo(correo)
        if self.dataBase.buscarCorreo(correo) == True:

            contra = self.dataBase.obtenerContrasenaPara(correo)
            mensaje = 'Por favor no vuelva a olvidar que su clave de ingreso es: ' + contra
            msg['from'] = 'valledevEPS@gmail.com'
            msg['to'] = correo
            msg['Subject'] = 'Recuperación de contraseña EPS'
            msg.attach(MIMEText(mensaje, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com: 587')
            server.starttls()
            server.login(msg['From'], 'bananiiiin') ##conexión con el servicio de correos
            server.sendmail(msg['From'], msg['To'], msg.as_string()) #envia mensaje
            server.quit()
            print("Mensaje enviado")
            return True
        else:
            return False

    def enviarDatosLogin(self,correo,contra,rol):
        msg = MIMEMultipart()
        mensaje = 'Usted ha sido registrado como: '+ rol + '\nCorreo registrado: ' + correo + '\nRecuerde que su contraseña es: ' + contra
        msg['from'] = 'valledevEPS@gmail.com'
        msg['to'] = correo
        msg['Subject'] = 'REGISTRO EXITOSO'
        msg.attach(MIMEText(mensaje, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        server.login(msg['From'], 'bananiiiin') ##conexión con el servicio de correos
        server.sendmail(msg['From'], msg['To'], msg.as_string()) #envia mensaje
        server.quit()
        print("Mensaje enviado")


    def cargarAdmin(self, correo): 
        query = self.dataBase.obtenerAdmin(correo)
        if query != None:
            ndoc= query[0]
            nom = query[1]
            ape = query[2]
            admin = Administrador("CC", ndoc, nom, ape, 3104290948, correo, "1" )
            return admin
        else:
            return None

    def cargarDoctor(self, correo):
        query =  self.dataBase.obtenerDoctor(correo)
        if query != None:
            ndoc= query[0]
            nom = query[1]
            ape = query[2]
            doc = Doctor("tipoDoc", ndoc, nom, ape, 3456789666, correo, "1")
            return doc
        else:
            return None

    def doctorPaciente(self,docDoctor,fecha,fecha2):
        query = self.dataBase.pacienteDoctor(docDoctor,fecha,fecha2)

        if query != None:
            docPacienteR = query[1]
            fechaR = query[2]
            token = self.recibirTokenHCCORE()
            #print("HOLAAA")
            headers = { 'Content-Type' : 'application/json', 'Authorization' : '{}'.format(token) }
            urlpaciente = 'http://34.95.198.251:3001/eps/getPaciente'
            body = {
            "idEntidad" : 1,
            "DNI" : 987654
            }
            body['DNI']=docPacienteR

            responsepac = requests.post(urlpaciente, data = json.dumps(body), headers = headers)
            #print("responsepac",responsepac)
            if responsepac.status_code == 200:
                paciente_json = responsepac.json()
                print(paciente_json)
                return (1,docPacienteR,fechaR,paciente_json['data']['nombrePaciente'])
            else:
                return (-1, None,None,None)



            return (1,docPacienteR,fechaR,paciente_json['data']['nombrePaciente'])
        else:
            print("SALTO")
            return (-1,None,None,None)

    def tipo_documento(self):
        return self.dataBase.obtener_tipo_documentos()


    def obtener_eps(self):
        return self.dataBase.eps()

    def obtener_espc(self):
        return self.dataBase.especializacion()

    def obtener_ciudades(self):
        return self.dataBase.ciudades()

    def recibirTokenHCCORE(self):
        url = 'http://34.95.198.251:3001/eps/sign'
        body = { "id":"1", "password":"ValleMedPassword"}
        headers = { 'Content-Type' : 'application/json' }

        response = requests.post(url,data=json.dumps(body),headers=headers)
        response_json = response.json()
        #print(response_json)
        token = response_json['token']
        #print(response.status_code)

        if response.status_code == 200:
            #print("BIEN")
            return token
        else:
            print("Fallo en conexión con la API")
            return response.status_code

    def agregarPaciente(self,nrodocumento,nombreCompleto,nacimiento,eCivil,telefono,sexo):
        token = self.recibirTokenHCCORE()
        
        url = 'http://34.95.198.251:3001/eps/createUser'
        headers = { 'Content-Type' : 'application/json', 'Authorization' : '{}'.format(token)}
        body = {
            "DNI" : 987654,
            "nombre" : "Diomedez Diaz",
            "fechaNacimiento" : "1950-12-25",
            "estadoCivil" : "soltero",
            "telefono" : 3224053212,
            "sexo" : "masculino",
            "idEntidad" : 1
        }
        
        url2 =  'http://34.95.198.251:3001/eps/createHC'
        body2 = {
            "DNI" : 987654,
            "idEntidad" : 1,
            "fisiologica" : {
                "lactancia" : " ",
                "iniciacionSexual" : " ",
                "ginecoObstretico" : "NO",
                "menarca" : "NORMAL",
                "embarazos" : "0",
                "partos" : "0",
                "abortos" : "0"
            },
            "antecedentes" : {
                "accidentes" : "Nacimiento",
                "antecedentesHereditarios" : "DIABETES",
                "enfermedadesInfancia" : "OTITIS",
                "intervencionesQuirurgicas" : " ",
                "alergias" : "NINGUNA",
                "inmunizacion" : "NINGUNA"
            }
        }
        
        body['DNI'] = int(nrodocumento)
        body2['DNI'] = int(nrodocumento)
        body['nombre'] = str(nombreCompleto)
        body['fechaNacimiento'] = str(nacimiento)
        body['estadoCivil'] = str(eCivil)
        body['telefono'] = int(telefono)
        body['sexo'] = str(sexo)
        
        
        #print(body)
        #print(headers)

        response = requests.post(url, data = json.dumps(body),headers=headers)
        
        print(response.status_code)

        if response.status_code == 200:
            response2 = requests.post(url2, data = json.dumps(body2),headers=headers)
            if response2.status_code == 200:
                #print ("Info:")
                #print(response.content)
                #print(response2.content)
                return 1
        else:
            #print(response.content)
            #print("Fallo en conexión con la API")
            return 2

    def insertarSolicitud(self,descripcion,estado,idmedico,nropaciente):
        medi = self.dataBase.insertarSolicitud(descripcion,estado,idmedico,nropaciente)
        return medi

    def mostrarSolicitudes(self):
        solicitud = self.dataBase.obtenerSolicitudes()
        solicitudes = []
        for i in solicitud:

            idPaciente = i[4]
            idMedico = i[5]
            descripcion = i[1]
            estado = i[3]
            justificacion = i[3]
            
            solicitudes.append(i)
                    #print()
        return solicitudes

    def obtenerSolicitudesActualizadas(self,data):
        solicitudes = []
        for i in data:
            idSolicitud = data[i]['idSolicitud']
            nuevoEstado = data[i]['nuevoEstado']
            justificacion = data[i]['justificacion']
            solicitud = []
            estado = True
            if nuevoEstado == 'Pendiente':
                nuevoEstado = data[i]['estadoActual']
                solicitud.append(idSolicitud)
                solicitud.append(nuevoEstado)
                #solicitud.append(justificacion)
                #solicitudes.append(solicitud)

                if justificacion == '':
                    solicitud.append(data[i]['detalles'])
                    solicitud.append('anterior')
                    solicitud.append(False)
                    solicitudes.append(solicitud)
                else:
                    solicitud.append(justificacion)
                    solicitud.append('')
                    solicitud.append(False)
                    solicitudes.append(solicitud)
                estado = False
                #return (idSolicitud,nuevoEstado,justificacion)
            else:
                solicitud.append(idSolicitud)
                solicitud.append(nuevoEstado)
                #solicitud.append(justificacion)
                #solicitudes.append(solicitud)
                if justificacion == '':
                    solicitud.append(data[i]['detalles'])

                    solicitud.append('')
                    solicitud.append(True)
                    solicitudes.append(solicitud)

                else:

                    solicitud.append(justificacion)
                    solicitud.append('')
                    solicitud.append(True)
                    solicitudes.append(solicitud)
                estado = True     
        return (solicitudes)
                #return (idSolicitud,nuevoEstado,justificacion)

    def actualizarSolicitud(self,idSolicitud,nuevoEstado,justificacion):
        solicitudes = self.dataBase.actualizarSolicitudes(idSolicitud,nuevoEstado,justificacion)
        return solicitudes

    def crearCita(self,motivo,idHClinica,fecha,idMedico):
        token = self.recibirTokenHCCORE()
        url = 'http://34.95.198.251:3001/eps/createCita' 
        headers = { 'Content-Type' : 'application/json', 'Authorization' : '{}'.format(token) }

        body = {
            "idEntidad" : 1,
            'idHistorioClinica': '',
            'fecha': "string",
            'motivo' : "string",
            'epsAgenda' : '',
            'idMedico' : '',
            'examenFisico' : {
                'estadoConciencia' : "string",
                'lenguaje' : "string",
                'auditivo' : "string",
                'agudezaVisual' : "string",
                'peso' : '',
                'estatura' : '',
                'facie' : "string",
                'edadRealAparente' : "string",
                'temperatura' : '',
                'actitud' : "string",
            },
            'habitos' : {
                'alimentacion' : "string",
                'apetito' : "string",
                'sed' : "string",
                'diuresis' : "string",
                'catarsisIntestinal' : "string",
                'sueno' : "string",
                'relacionesSexuales' : "string",
                'alcohol' : "string",
                'tabaco' : "string",
                'drogas' : "string",
                'medicacion' : "string",
            },
            'diagnostico' :{
                'diagnostico' : "",
                'examenes': {},
                'tratamientos':{}
                }
            }

        body['idHistorioClinica']=idHClinica
        body['fecha']=fecha
        body['motivo']=motivo
        body['idMedico']=idMedico

        responsepac = requests.post(url, data = json.dumps(body), headers = headers)




    def getHCPaciente(self, nrodocumento):
        token = self.recibirTokenHCCORE()
        datax = {}
        print("ANTES TOKEN")
        headers = { 'Content-Type' : 'application/json', 'Authorization' : '{}'.format(token) }
        urlpaciente = 'http://34.95.198.251:3001/eps/getPaciente'
        url = 'http://34.95.198.251:3001/eps/getHC'
        body = {
            "idEntidad" : 1,
            "DNI" : 987654
        }

        body['DNI'] = int(nrodocumento)
        #### request paciente----------------------------------  
        responsepac = requests.post(urlpaciente, data = json.dumps(body), headers = headers)
        if responsepac.status_code == 200:
            paciente_json = responsepac.json()
            print (paciente_json)
            datax['paciente'] = paciente_json

        else:
            return (3, responsepac)


        #####---------------------------------

        response = requests.post(url, data = json.dumps(body), headers = headers)
        response_json = response.json()
        print ("Hola Amigo otoya")
        print("Primer response: {}".format(response_json) )
        print("response: {}".format(response))
        if response.status_code == 200:
            if 'status' in response_json:
                if (response_json['status'] == "DECLINED"):
                    if response_json['message'] == "Historia clinica no existe":
                        return (3, response_json)
            else:
                
                citas = []
                urlcitas = 'http://34.95.198.251:3001/eps/getCitas'
                bodycitas = {'idEntidad' : 1, 'DNI' : int(nrodocumento) }
                responsecitas = requests.post(urlcitas, data = json.dumps(bodycitas), headers = headers)
                responsecitas_json = responsecitas.json()
                
                #print("segundo response: {}".format(responsecitas_json) )
            
                if (responsecitas_json['status'] == "OK"):
                    for i in responsecitas_json['data']:
                        urlcita = 'http://34.95.198.251:3001/eps/getCitaMedica'
                        body2 = {"idEntidad" : 1,"idCitaMedica" : i["idConsulta"] }
                        responsecita = requests.post(urlcita, data = json.dumps(bodycitas), headers = headers)
                        responsecita_json = responsecita.json()
                        citas.append(responsecita_json)
    
                    return (1, response_json)
                elif (responsecitas_json['status'] == "ERROR") and (responsecitas_json['message'] == "No hay citas"):
                    datay = response_json['data']
                    del datay['antecedentes']['id']
                    del datay['fisiologica']['id']
                    datax['antecedentes'] = datay['antecedentes']
                    datax['fisiologica'] = datay['fisiologica']
                    del datax['paciente']['token']
                    print(datax)
                    pdf_name = self.JSONtoPDF(datax)
                    return (1, pdf_name)

                else:
                    #print("Return 4")
                    return (4, response_json)
        else:
            print(response.content)
            #print("Fallo en conexión con la API")
            return (2, response_json)

    
    def JSONtoPDF(self, data):
        #Escribir en un pdf usando FPDF
        pdfwriter = fpdf.FPDF(orientation= 'P', unit= 'mm', format = 'A4')
        pdfwriter.add_page()
        pdfwriter.set_font('arial', size = 12)
        # centrado de título
        pdfwriter.cell(w = 80)   
        #Titulo
        pdfwriter.cell(20, 10, "Historia Clínica", 0, 2, 'C')
        pdfwriter.cell(20, 10, "Paciente: " + data['paciente']['nombrePaciente'], 0, 2, 'C')
        pdfwriter.ln(h='')
        pdfwriter.cell(100, 10, "Información del paciente: ", 0, 1)
        contCols = 0
        print ("Paciente: ")
        for i in data['paciente']:
            if contCols == 0:
                pdfwriter.cell(95, 10, str(i) + ": "+ str(data['paciente'][i]) , 1, 0) 
                contCols = 1
            else:
                if contCols == 1:
                    pdfwriter.cell(95, 10, str(i) + ": "+ str(data['paciente'][i]) , 1, 1) 
                    contCols = 0
            print("     " + i)
        print ("Antecedentes: ")
        pdfwriter.ln(h='')
        pdfwriter.cell(80, 10, "Antecedentes: ", 0, 1)
        for i in data["antecedentes"]:
            pdfwriter.multi_cell(190, 10, i+ ": "+ str(data["antecedentes"][i]) , 1, 1) 
            print("     " + i)

        print ("Fisiologica: ")
        contCols = 0
        pdfwriter.ln(h='')
        pdfwriter.cell(80, 10, "Fisiológica: ", 0, 1)
        for i in data['fisiologica']:
            if contCols == 0:
                pdfwriter.cell(95, 10, i+ ": "+ data['fisiologica'][i] , 1, 0) 
                contCols = 1
            else:
                if contCols == 1:
                    pdfwriter.cell(95, 10, i+ ": "+ data['fisiologica'][i] , 1, 1) 
                    contCols = 0
            print("     " + i)
        pdfwriter.ln(h='')
        pdfwriter.ln(h='')
        pdfwriter.cell(80, 10, "Citas Médicas: ", 0, 1)
        j = 0
        contCols = 0
        if 'citasMedicas' in data:
            while (j <len (data['citasMedicas'])):
                pdfwriter.cell(80, 10, "Cita #" + str(j), 0, 1)
                for x in data['citasMedicas'][j]:
                    
                    if x == "medico":
                        pdfwriter.cell(190, 10, "Médico: ", 1, 1, 'C')
                        contCols = 0
                        for m in data['citasMedicas'][j][x]:
                            if contCols == 0:
                                pdfwriter.cell(95, 10, m+ ": "+ data['citasMedicas'][j][x][m] , 1, 0) 
                                contCols = 1
                            else:
                                if contCols == 1:
                                    pdfwriter.cell(95, 10, m+ ": "+ data['citasMedicas'][j][x][m] , 1, 1) 
                                    contCols = 0
                    elif x == "examenFisico":
                        pdfwriter.cell(190, 10, "Exámen físico: ", 1, 1, 'C')
                        contCols = 0
                        for n in data['citasMedicas'][j][x]:
                            if contCols == 0:
                                pdfwriter.cell(95, 10, n+ ": "+ data['citasMedicas'][j][x][n] , 1, 0) 
                                contCols = 1
                            else:
                                if contCols == 1:
                                    pdfwriter.cell(95, 10, n+ ": "+ data['citasMedicas'][j][x][n] , 1, 1) 
                                    contCols = 0
                    elif x == "examenSegmentario":
                        pdfwriter.ln(h='')
                        pdfwriter.cell(190, 10, "Exámen segmentario: ", 1, 1, 'C')
                        contCols = 0
                        for o in data['citasMedicas'][j][x]:
                            if contCols == 0:
                                pdfwriter.cell(95, 10, o+ ": "+ data['citasMedicas'][j][x][o] , 1, 0) 
                                contCols = 1
                            else:
                                if contCols == 1:
                                    pdfwriter.cell(95, 10, o+ ": "+ data['citasMedicas'][j][x][o] , 1, 1) 
                                    contCols = 0
                    elif x == "examenes":
                        pdfwriter.ln(h='')
                        if len(data['citasMedicas'][j][x]) == 0:
                            pdfwriter.cell(190, 10, "Exámenes: No hay exámenes para ver", 1, 1, 'C')
                        else:
                            pdfwriter.cell(190, 10, "Exámenes: ", 1, 1, 'C')
                        contCols = 0
                        k = 0
                        while k < len(data['citasMedicas'][j][x]):
                            
                            pdfwriter.cell(190, 10, "Exámen #" + str(k), 1, 1)
                            contCols = 0
                            for p in data['citasMedicas'][j][x][k]:
                                if contCols == 0:
                                    pdfwriter.cell(95, 10, p+ ": "+ str(data['citasMedicas'][j][x][k][p]) , 1, 0) 
                                    contCols = 1
                                else:
                                    if contCols == 1:
                                        pdfwriter.cell(95, 10, str(p)+ ": "+ str(data['citasMedicas'][j][x][k][p]) , 1, 1) 
                                        contCols = 0
                            k += 1

                    elif x == "habitos":
                        pdfwriter.cell(190, 10, "Habitos:", 1, 1, 'C')
                        contCols = 0
                        for o in data['citasMedicas'][j][x]:
                            if contCols == 0:
                                pdfwriter.cell(95, 10, o+ ": "+ data['citasMedicas'][j][x][o] , 1, 0) 
                                contCols = 1
                            else:
                                if contCols == 1:
                                    pdfwriter.cell(95, 10, o+ ": "+ data['citasMedicas'][j][x][o] , 1, 1) 
                                    contCols = 0
                    elif x == "diagnostico":
                        pdfwriter.multi_cell(190, 10, "Diagnóstico: "+ data['citasMedicas'][j][x]["diagnostico"] , 1, 1)
                        pdfwriter.multi_cell(190, 10, "Tratamientos:", 1, 1, 'C') 
                        w = 0
                        while w < len(data['citasMedicas'][j][x]["tratamientos"]):
                            pdfwriter.cell(190, 10, "Tratamiento #" + str(w), 1, 1, 'C') 
                            pdfwriter.cell(190, 10, "Concepto" + ": "+ data['citasMedicas'][j][x]["tratamientos"][w]['concepto'] , 1, 1)
                            pdfwriter.cell(190, 10, "Medicamentos:", 1, 1) 
                            p = 0
                            while p < len(data['citasMedicas'][j][x]["tratamientos"][w]['medicamentos']) :
                                pdfwriter.cell(190, 10, "Medicamento #" + str(p), 1, 1) 
                                pdfwriter.multi_cell(190, 10, "Nombre" + ": "+ data['citasMedicas'][j][x]["tratamientos"][w]['medicamentos'][p]['nombre'] , 1, 1)
                                pdfwriter.multi_cell(190, 10, "Contenido" + ": "+ data['citasMedicas'][j][x]["tratamientos"][w]['medicamentos'][p]['contenido'] , 1, 1)
                                p += 1
                            w += 1
                            
                    else:
                        pdfwriter.multi_cell(190, 10, x+ ": "+ str(data['citasMedicas'][j][x]) , 1, 1) 
                        contCols = 1
                    
                    print (data['citasMedicas'][j][x])
                pdfwriter.ln(h='')
                j +=1 
            
        #Crea el nombre de documento con el id del paciente
        pdfname = str(data['paciente']['identificacion']) +".pdf"
        pdfwriter.output(pdfname, 'F')


        #3print(data)
        return pdfname

