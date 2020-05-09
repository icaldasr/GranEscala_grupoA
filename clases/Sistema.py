#Sistema.py
#Autor: Luis Miguel Oviedo
#smtp lib para envío de mensajes en recuperacion de la clave de ingreso
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
##dentro del proyecto
from clases.Gestor import Gestor
from clases.SolicitudM import SolicitudM
from clases.HistoriaClinica import HistoriaClinica
from clases.Administrador import Administrador
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

    def tipo_documento(self):
        return self.dataBase.obtener_tipo_documentos()


    def obtener_eps(self):
        return self.dataBase.eps()

    def obtener_espc(self):
        return self.dataBase.especializacion()

    def obtener_ciudades(self):
        return self.dataBase.ciudades()
