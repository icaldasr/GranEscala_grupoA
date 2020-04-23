#Sistema.py
#Autor: Luis Miguel Oviedo

from clases.Gestor import Gestor
from clases.SolicitudM import SolicitudM
from clases.HistoriaClinica import HistoriaClinica

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


        
        

    def agregarDoctor(self, doctor):
        self.doctores.append(doctor)
        #dataBase.agregarDoctor(doctor)

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
