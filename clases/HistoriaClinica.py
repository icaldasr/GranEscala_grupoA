#HistoriaClinica.py

from clases.Cita import Cita

class HistoriaClinica():
    def __init__(self, tipodoc, ndocpac):  ##valores de id del usuario
        self.citasRealizadas = []
        self.tipoDocPaciente = tipodoc
        self.ndocPaciente = ndocpac 

    def agregarCita(self, cit):
        self.citasRealizadas.append(cit)