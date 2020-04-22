#Usuario.py

from clases.Persona import Persona

class Usuario(Persona):
    def __init__(self, tipoDoc, numDoc, nom, ap, cel, nomusr, cla):
        Persona.__init__(self, tipoDoc, numDoc, nom, ap, cel)
        self.usuario = nomusr
        self.clave = cla ## ??

    def setUsuario(self, nomusr):
        self.usuario = nomusr

    def getUsuario(self):
        return self.usuario

    def setClave(self, cla):
        self.clave = cla

    def getClave(self):
        return self.clave