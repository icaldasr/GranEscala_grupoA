from wtforms import Form, SelectField, BooleanField, TextField, DateField,StringField, PasswordField, validators, IntegerField
from wtforms_validators import ActiveUrl, AlphaSpace, AlphaNumeric, Integer
from wtforms.fields.html5 import EmailField

from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(Form):
	
    nombres = StringField('Nombres', 
        validators = [DataRequired(),
        AlphaSpace(message = 'Sólo debe contener letras')
        ])

    apellidos = StringField('Apellidos',
        validators = [DataRequired(),
        AlphaSpace(message = 'Sólo debe contener letras')
        ])

    tipoDoc = SelectField('Tipo de Documento',
       choices=[('CC', 'Cédula de Ciudadania'), ('CE', 'Cédula de Extranjería'), ('PP', 'Pasaporte')],
       validators = [DataRequired()])
        #FALTA VALIDACIÓN CON LA BASE
    numDoc = StringField('Número de documento',
        validators = [DataRequired(),
        AlphaNumeric(message = 'Sólo puede contener números y letras')
        ])

    especialidad = SelectField('Especialidad',
        choices=[('100', 'Alergia e Inmunologpia'),
        ('101','Anatomía Patológica'),
        ('102','Anestesiología'),
        ('103','Cardiología'),
        ('104','Cardiólogo Infantil'),
        ('105','Cirugía General'),
        ('106','Cirugía Cardiovascular'),
        ('107','Cirugía Infantil'),
        ('108','Cirugía Plástica'),
        ('109','Coloproctología'),
        ('110','Dermatología'),
        ('111','Endocrinología'),
        ('112','Endocrinologia Infantil'),
        ('113','Fisiatría'),
        ('114','Gastroenterología'),
        ('115','Gastroenterólogo Infantil'),
        ('116','Geriatría'),
        ('117','Ginecología'),
        ('118','Infectología'),
        ('119','Medicina General'),
        ('120','Nefrología'),
        ('121','Neumonología'),
        ('122','Neurología'),
        ('123','Nutrición'),
        ('124','Obstetricia'),
        ('125','Oftalmología'),
        ('126','Oncología'),
        ('126','Oncología Infantil'),
        ('127','Ortopedia y Traumatología'),
        ('128','Otorrinolaringología'),
        ('129','Pediatría'),
        ('130','Psiquiatría'),
        ('131','Urología')
        ])

    telefono = IntegerField('Número de teléfono',
        validators=[DataRequired(message='Sólo debe contener números.')
        ])
    
    fechaNacimiento = DateField('Fecha de Nacimiento',format='%Y-%m-%d',
        validators=[DataRequired()
        ])

    genero = SelectField('Género',
        choices=[('FF','Mujer'),('HH','Hombre'),('NA','No Aplica')],
        validators = [DataRequired()])

    correo = EmailField('Correo Electrónico',
        validators = [DataRequired()])

    contrasena = PasswordField('Nueva Contraseña',
        validators = [DataRequired(),
        EqualTo('confirmarContrasena', message='Las contraseñas deben coincidir.')
        ])

    confirmarContrasena = PasswordField('Repetir contraseña',
        validators = [DataRequired()])


