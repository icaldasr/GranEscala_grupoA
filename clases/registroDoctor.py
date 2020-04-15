from flask import Flask
from flask import request
from flask import render_template

from flask_mysqldb import MySQL

import formRegistroDoctor

import sys

app = Flask(__name__) #Nuevo objeto

#Conección con la base de datos 
app.config['MYSQL_USER'] = '203256'
app.config['MYSQL_PASSWORD'] = 'juancamilo99'
app.config['MYSQL_HOST'] = 'mysql-historiasclinicas.alwaysdata.net'
app.config['MYSQL_DB'] = 'historiasclinicas_bd'

mysql = MySQL(app)

@app.route('/registroDoctor', methods=['GET', 'POST'])
	
def registroDoctor():

    form = formRegistroDoctor.RegistrationForm(request.form)
    cur = mysql.connection.cursor()
    if request.method == 'POST' and form.validate():

        nombre = form.nombres.data
        apellidos = form.apellidos.data
        documento = form.numDoc.data
        especialidad = form.especialidad.data
        correo = form.correo.data
        contrasena = form.contrasena.data

        try:
        	cur.execute('''INSERT INTO medicos VALUES (%s,3,%s,%s,%s)''',(documento,nombre,apellidos,especialidad))
        	cur.execute('''INSERT INTO login VALUES (%s,%s,%s)''',(correo,contrasena,documento))

        except mysql.connection.IntegrityError as err:
        	print("Error: {}".format(err))
        	return 'Usuario duplicado'

        mysql.connection.commit()
        cur.close()
        print(especialidad)

        return 'BIEN'

    return render_template('registroDoctor.html', form=form)

if __name__ == '__main__':
	app.run(debug = True, port = 5500) 