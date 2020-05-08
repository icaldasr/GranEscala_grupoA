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


    def buscarCorreo(self,correo):
        self.cursor.execute("SELECT count(*) FROM login where correo = %s",correo)
        temp = self.cursor.fetchone()[0]
        if temp == 1:
            
            return True
        else:
            return False

    def obtenerContrasenaPara(self, correo):
        self.cursor.execute(
            "(SELECT  nombres, correo, contrasena, tipo FROM login inner JOIN medicos USING (correo))  UNION (select nombres, correo, contrasena, tipo from login INNER JOIN administrador USING (correo))"
        )
        temp = self.cursor.fetchall()
        #print (temp)
        if temp == None:
            return None
        else:
            for i in temp:
                if i[1] == correo:
                    return i[2]
                    
    def obtenerAdmin(self, correo):
        self.cursor.execute(
            "select nro_documento, nombres, apellido, correo, contrasena from login INNER JOIN administrador USING (correo) where correo = %s" , correo
        )
        temp = self.cursor.fetchone()
        if temp == None:
            return None
        else:
            return temp

    def insertarDoctor(self, tipodoc, nrodocumento, nombre, apellido, ideps, idespecializacion, rh, correo, nacimiento, tel, departamento, ciudad, bario, sexo):
        self.cursor.execute(
            "insert into medicos (id_tip, nro_documento, nombres, apellido, id_eps, id_espc, correo) values (%d, %d, %s, %s, %d, %d, %s)" , tipodoc, nrodocumento, nombre, apellido, ideps, idespecializacion, correo
        )
        self.conexion.commit()
        self.cursor.execute(
            "insert into login (correo, contrasena, tipo) values (%s, '123456', 'medico' )", correo
        )
        self.conexion.commit()

    def insertarAdministrador(self, nrodocumento, nombre, apellido, correo,celular,tipoDoc,contra):
        
        self.cursor.execute('''INSERT INTO administrador VALUES (%s,%s,%s,%s,%s,%s)''', (nrodocumento, nombre, apellido, correo,celular,tipoDoc))
        self.cursor.execute('''INSERT INTO login VALUES (%s, %s, 'administardor')''',(correo,contra))
        self.conexion.commit()

    
    def obtener_tipo_documentos(self):
        self.cursor.execute(
            """
            select descripcion from tipo_documento
            """
        )
        return self.cursor.fetchall()