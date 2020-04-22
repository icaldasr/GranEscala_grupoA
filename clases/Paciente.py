#Paciente.py

from clases.Persona import Persona

class Paciente(Persona):
    def __init__(self, tipoDoc, numDoc, nom, ap, cel):
        Persona.__init__(self, tipoDoc, numDoc, nom, ap, cel)
        self.historiaClinica = HistoriaClinica(tipoDoc, numDoc)
        self.citasPendientes  = []

    def getHistoriaClinica(self):
        return self.historiaClinica

    def agregarCitaHC(self, cit):
        if self.historiaClinica != None:
            self.historiaClinica.agregarCita(cit)
        else: 
            print("Se debe crear historia clínica para este paciente")

    def agregarCitaPendiente(self, cit):
        self.citasPendientes.append(cit)