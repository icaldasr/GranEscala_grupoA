#Administrador.py

from clases.Usuario import Usuario

class Administrador(Usuario):
    def __init__(self, tipoDoc, numDoc, nom, ap, cel, nomusr, cla):
        Usuario.__init__(self, tipoDoc, numDoc, nom, ap, cel, nomusr, cla)
        self.solMactiva = None

    def agregarDoctor(self,  tipoDoc, numDoc, nom, ap, cel, nomusr, cla):
        #Contraseña aleatoria
        Sistema.getInstance().agregarDoctor(Doctor(tipoDoc, numDoc, nom, ap, cel, nomusr, cla))

    def darDeBajaDoctor(self, tipodoc, numdoc):
        Sistema.getInstance().darDeBajaDoctor(tipodoc, numdoc)

    def gestionarSolicitudM(self):
        self.solactiva = Sistema.getSolicitud()

    def aceptarSolicitud(self):
        self.solMactiva.setEstado("aceptada")
        self.solMactiva = None

    def rechazarSolicitud(self):
        self.solMactiva.setEstado("rechazada")
        self.solMactiva = None

    def crearCitaDisponible(self, fecha, hora, doc):
        idC = Sistema.nuevoIdCita()
        Sistema.nuevaCita(Cita(idC, fecha, hora, doc))