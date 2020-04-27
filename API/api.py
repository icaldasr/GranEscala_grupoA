import pymysql
import json
from flask import Flask
from obtener_horarios import obtener_consultorios, generar_horarios

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
        consultorios = obtener_consultorios(consulta)
        horarios = generar_horarios(consultorios, consulta)

        return json.dumps(horarios)
    else:
        return json.dumps({"mensaje":"no se encontraron resultados"})





@app.route('/ips')
def obtener_ips():
    global cursor
    cursor.execute(
        """
        select id_ips, nombre, direccion from ips
        """
    )
    consulta = cursor.fetchall()
    if len(consulta) != 0:
        temp = list()
        ips = {}
        contador = 0
        while contador < len(consulta):
            plantilla = {
                'id ips': None,
                'nombre': None,
                'direccion': None
            }
            plantilla['nombre'] = consulta[contador][1]
            plantilla['direccion'] = consulta[contador][2]
            plantilla['id ips'] = consulta[contador][0]
            temp.append(plantilla)
            contador = contador + 1
        ips['ips'] = temp
        return json.dumps(ips)
    else:
        return json.dumps({'mensaje':"no hay ips en la base de datos"})









if __name__ == '__main__':
    app.run(debug=True)