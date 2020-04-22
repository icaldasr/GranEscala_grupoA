#Persona.py


class Persona():
    def __init__(self, tipoDoc, numDoc, nom, ap, cel):
        self.tipoDocumento = tipoDoc   
        self.numeroDocumento = numDoc
        self.nombre = nom
        self.apellido = ap
        self.celular = cel

    def setTipoDoc(self, tipo):
        self.tipoDocumento = tipo

    def getTipoDoc(self):
        return self.tipoDocumento

    def setNumeroDoc(self, num):
        self.numeroDocumento = num

    def getNumeroDoc(self):
        return self.numeroDocumento

    def setNombre(self, nom):
        self.nombre = nom

    def getNombre(self):
        return self.nombre

    def setApellido(self, ap):
        self.apellido = ap

    def getApellido(self):
        return self.apellido

    def setCelular(self, cel):
        self.celular = cel

    def getCelular(self):
        return self.celular