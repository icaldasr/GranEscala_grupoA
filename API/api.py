import pymysql
from flask import Flask

#conexion base de datos
conexion = pymysql.Connect(host='mysql-historiasclinicas.alwaysdata.net', 
                           user='203256', password='juancamilo99', db='historiasclinicas_bd')
cursor = conexion.cursor()
#servidor flask
app = Flask(__name__)


@app.route('/horarios/<string:ips>/<string:espc>')
def obtener_horarios(ips, espc):
    global cursor
    cursor.execute(
        """
        select fecha_inicial, fecha_final, nro_consultorio from especializaciones inner join medicos on (especializaciones.id_especializacion = medicos.id_espc)
        inner join consultorios on (medicos.nro_documento = consultorios.id_medico) inner join ips on (consultorios.id_Ips = ips.id_ips)
        where ips.nombre = %s and especializaciones.nombre = %s
        """,
        (ips, espc)
    )
    a = cursor.fetchall()
    print(ips)
    return espc









if __name__ == '__main__':
    app.run(debug=True)