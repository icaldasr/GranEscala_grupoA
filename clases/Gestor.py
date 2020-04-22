#Gestor.py

class Gestor():
    instance = None
    @staticmethod
    def getInstance():
        if not Gestor.instance:
            Gestor.__init__()
        return Gestor.instance

    
    def __init__(self):
        if Gestor.instance != None:
            raise Exception("Esta es una instancia unica")
        else: 
            Gestor.instance = self
            self.name = "MySQLDataBase for EPS"

    def validar(self, usuario, clave):
        ##validar usaurios en base de datos
        return 0

    def actualizarP(self, paciente):
        #actualizar valores con la info de paciente
        print ("hola1")

    def actualizarC(self, cita):
        #actualizar valore scon info de cita
        print ("hola1")

    def nuevoIdCita(self):
        #return nuevo id para una cita diferente a los ya creados. 
        print ("hola1")
    
    def nuevoIdSolicitudM(self):
        #return nuevo id para una solicitud de medicamentos
        print ("hola1")