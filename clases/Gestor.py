#Gestor.py

import pymysql

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
            self.conexion = pymysql.connect(host='mysql-historiasclinicas.alwaysdata.net',  user='203256', password='juancamilo99', db='historiasclinicas_bd')
            self.cursor = self.conexion.cursor()


    def getLoginInfo(self):
        self.cursor.execute(
            "(SELECT nombres, correo, contrasena, tipo FROM login inner JOIN medicos USING (correo))  UNION (select nombres, correo, contrasena, tipo from login INNER JOIN administrador USING (correo))"
        )
        temp = self.cursor.fetchall()
        #print (temp)
        if temp == None:
            return None
        else:
            return temp


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