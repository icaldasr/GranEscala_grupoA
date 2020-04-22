#Medicamento.py


class Medicamento():
    def __init__(self, nom, cod, desc, adv):
        self.nombre = nom
        self.codigo = cod
        self.descripcion = desc
        self.advertencias = adv
    
    def setNombre(self, nom):
        self.nombre = nom

    def getNombre(self):
        return self.nombre
    
    def setCodigo(self, cod): 
        self.codigo = cod

    def getCodigo(self):
        return self.codigo

    def setDescripcion(self, desc):
        self.descripcion = desc

    def getDescripción(self):
        return self.descripcion

    def setAdvertencias(self, adv):
        self.advertencias = adv

    def getAdvertencias(self):
        return self.advertencias