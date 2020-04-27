import pymysql
import json
from flask import Flask
from datetime import datetime
from datetime import timedelta
from obtener_horarios import obtener_consultorios

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
        select nro_consultorio, fecha_inicial, fecha_final, horarios.fecha, medicos.nro_documento, medicos.nombres, especializaciones.nombre from especializaciones inner join medicos on (especializaciones.id_especializacion = medicos.id_espc)
        inner join consultorios on (medicos.nro_documento = consultorios.id_medico) inner join ips on (consultorios.id_Ips = ips.id_ips)
        inner join horarios on (horarios.id_consultorio = consultorios.nro_consultorio)
        where ips.nombre = %s and especializaciones.nombre = %s order by nro_consultorio, horarios.fecha
        """,
        (ips, espc)
    )
    consulta = cursor.fetchall()
    if len(consulta) != 0:
        #variables obtencion de consultorios
        consultorios = obtener_consultorios(consulta)
        #variables resultado final
        horarios = {}
        contador2 = 0
        contador = 0
        print(consultorios)
        # while contador < len(consultorios):
        #     while contador2 < len(consulta):
        #         if consulta[contador2][0] == consultorios[contador]:

        return 'a'      
    else:
        return json.dumps({"mensaje":"no se encontraron resultados"})









if __name__ == '__main__':
    app.run(debug=True)