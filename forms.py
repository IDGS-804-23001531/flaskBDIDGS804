from wtforms import Form
from flask_wtf import FlaskForm

from wtforms import StringField, IntegerField, TextAreaField, SelectField, HiddenField
from wtforms import EmailField
from wtforms import validators

class UserForm(Form):
    id = IntegerField("id", [
        validators.optional()
    ])
    nombre=StringField("nombre", [
        validators.DataRequired(message="El nombre es requerido"),
        validators.length(min=4,max=20, message='requiere min=4 max=20')
    ])
    apellidos=StringField("apellidos", [
        validators.DataRequired(message="El apellido es requerido")
    ])
    email=EmailField("email", [
        validators.Email(message="El email es requerido"),
        validators.Email(message='Ingrese un email valido')
    ])
    telefono=StringField("telefono", [
        validators.DataRequired(message="El telefono es requerido")
    ])

class MaestroForm(Form):
    matricula = IntegerField("matricula", [
        validators.Optional()
    ])
    nombre=StringField("nombre", [
        validators.DataRequired(message="El nombre es requerido"),
        validators.length(min=4,max=20, message='requiere min=4 max=20')
    ])
    apellidos=StringField("apellidos", [
        validators.DataRequired(message="El apellido es requerido")
    ])
    especialidad = StringField("especialidad", [
        validators.DataRequired(message="La especialidad es requerido")
    ])
    email=EmailField("email", [
        validators.Email(message="El email es requerido"),
        validators.Email(message='Ingrese un email valido')
    ])

class CursoForm(Form):
    id = IntegerField("id")

    nombre = StringField("nombre", [
        validators.DataRequired(message="El nombre del curso es requerido"),
        validators.length(min=4, max=30, message="requiere min=4 max=30")
    ])

    descripcion = TextAreaField("descripcion", [
        validators.DataRequired(message="La descripción es requerida"),
        validators.length(min=10, max=200, message="requiere min=10 max=200")
    ])

    maestro_id = SelectField("maestro_id",
        coerce=int,
        validators=[
            validators.DataRequired(message="El maestro es requerido")
        ]
    )

class InscripcionForm(Form):
    curso_id = HiddenField("curso_id")
    alumno_id = SelectField("alumno_id", coerce=int)