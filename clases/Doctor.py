#Doctor.py

from clases.Usuario import Usuario

class Doctor(Usuario):
    def __init__(self, tipoDoc, numDoc, nom, ap, cel, nomusr, cla):
        Usuario.__init__(self, tipoDoc, numDoc, nom, ap, cel, nomusr, cla)
        self.citaActual = None

    def finalizarCita(self):
        self.citaActual.finalizarCita()
        self.citaActual = None