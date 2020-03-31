import pymysql

class base_datos():
    def __init__(self):
        self.conexion = pymysql.Connect(host='mysql-historiasclinicas.alwaysdata.net', 
        user='203256', password='juancamilo99', db='historiasclinicas_bd')

        self.cursor = self.conexion.cursor()

base = base_datos()