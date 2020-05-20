#SolicitudM.py
#Autor: Luis Miguel Oviedo L

from clases.Medicamento import Medicamento
from clases.Paciente import Paciente
from clases.Doctor import Doctor

class SolicitudM():
    def __init__(self, i, med, pac, doc):
        self.id = i
        self.medicamento = med
        self.paciente = pac
        self.doc = doc
        self.estado = "esperando"
        self.comentarios = ""

    def setEstad(self, est):
        self.estado = est
    
    def getEstado(self):
        return self.estado

    def setComentarios(self, com):
        self.comentarios = com

    def getComentarios(self):
        return self.comentarios