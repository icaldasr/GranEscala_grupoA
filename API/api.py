import pymysql
from flask import Flask

conexion = pymysql.Connect(host='mysql-historiasclinicas.alwaysdata.net', 
                           user='203256', password='juancamilo99', db='historiasclinicas_bd')
cursor = conexion.cursor()

app = Flask(__name__)









if __name__ == '__main__':
    app.run(debug=True)