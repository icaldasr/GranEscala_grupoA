#Cita.py

from clases.Paciente import Paciente
from clases.Doctor import Doctor
from clases.Medicamento import Medicamento

class Cita():
    def __init__(self, i, fecha, hora, doc):
        self.id = i
        self.fecha = fecha
        self.hora = hora
        self.doctor = doc
        self.medicamentos = []
        self.observaciones = ""
        self.incapacidad = ""
        self.sintomas = ""
        self.enfermedad = ""
        self.examenes = []
        self.remision = []
        self.paciente = None
        self.estado = "disponible"

    def setId(self, i):
        self.id = i

    def getId(self):
        return self.id

    def setFecha(self, fec):
        self.fecha = fec

    def getFecha(self):
        return self.fecha

    def setHora(self, hor):
        self.hora = hor

    def getHora(self):
        return self.hora

    def getDoctor(self): 
        return self.doctor

    def addMedicamento(self, medic):
        self.medicamentos.append(medic)

    def getMedicamento(self, i):
        if len(self.medicamentos) != 0:
            return self.medicamentos[i]
        else: 
            return None
    
    def setObservaciones(self, obs):
        self.observaciones = obs
    
    def getObservaciones(self):
        return self.observaciones

    def setIncapacidad(self, inc):
        self.incapacidad = inc

    def getIncapacidad(self):
        return self.incapacidad
    
    def setSintomas(self, sin):
        self.sintomas = sin
    
    def getSintomas(self):
        return self.sintomas

    def setEnfermedad(self, enf):
        self.enfermedad =enf

    def getEnfermedad(self):
        return self.enfermedad

    def addExamen(self, ex):
        self.examenes.append(ex)
    
    def getExamen(self, i):
        if len(self.examenes) != 0:
            return self.examenes[i]
        else:
            return None

    def addRemision(self, rem):
        self.remision.append(rem)

    def getRemision(self,i):
        if len(self.remision) != 0:
            return self.remision[i]
        else:
            return None

    def setPaciente(self, pac):
        self.paciente = pac

    def getPaciente(self):
        return self.paciente

    def setEstado(self, est):
        self.estado = est

    def getEstado(self):
        return self.estado

    def finalizarCita(self):
        self.setEstado("finalizada")
        for i in self.medicamentos:
            Sistema.crearSolicitudM(i, self.paciente, self.doctor)  