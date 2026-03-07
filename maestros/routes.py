from . import maestros

from flask import render_template,request,redirect,url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
import forms
from flask_migrate import Migrate
#from maestros.routes import maestros,maestros
from models import db
from models import Alumnos, Maestros, Curso

@maestros.route('/perfil/<nombre>')
def perfil(nombre):
    return f"Perfil de {nombre}"

@maestros.route("/maestros", methods=['GET','POST'])
@maestros.route("/index")
def index():
    create_form=forms.UserForm(request.form)
    maestros=Maestros.query.all()
    return render_template("maestros/listadoMaes.html", form=create_form, maestros=maestros)

@maestros.route("/nuevo", methods=['GET', 'POST'])
def nuevo():
    create_form = forms.MaestroForm(request.form)
    if request.method == 'POST':
        if create_form.validate():
            nuevo_maestro = Maestros(
                matricula=create_form.matricula.data,
                nombre=create_form.nombre.data,
                apellidos=create_form.apellidos.data,
                especialidad=create_form.especialidad.data,
                email=create_form.email.data
            )
            db.session.add(nuevo_maestro)
            db.session.commit()
            return redirect("/maestros")
    return render_template("maestros/Maestros.html", form=create_form)

@maestros.route("/modificar", methods=['GET','POST'])
def modificar():
	create_form = forms.MaestroForm(request.form)
	if request.method == 'GET':
		id = request.args.get('id')
		# select * from maestros where matricula == id
		maes1 = db.session.query(Maestros).filter(Maestros.matricula == id).first()
		create_form.matricula.data = request.args.get('id')
		create_form.nombre.data = maes1.nombre
		create_form.apellidos.data = maes1.apellidos
		create_form.especialidad.data = maes1.especialidad
		create_form.email.data = maes1.email

	if request.method == 'POST':
		id = create_form.matricula.data
		# select * from maestros where matricula == id
		maes1 = db.session.query(Maestros).filter(Maestros.matricula == id).first()
		maes1.matricula = id
		maes1.nombre = create_form.nombre.data
		maes1.apellidos = create_form.apellidos.data
		maes1.especialidad = create_form.especialidad.data
		maes1.email = create_form.email.data

		# db.session.add(maes1)
		db.session.commit()
		return redirect(url_for('maestros.index'))
	return render_template("maestros/modificarMaes.html", form=create_form)

@maestros.route("/detalles", methods=['GET','POST'])
def detalles():
	create_form=forms.MaestroForm(request.form)
	if request.method=='GET':
		id=request.args.get('id')
		# select * from alumnos where id == id
		maes1=db.session.query(Maestros).filter(Maestros.matricula==id).first()
		id=request.args.get('id')
		nombre=maes1.nombre
		apellidos=maes1.apellidos
		email=maes1.email
		cursos = db.session.query(Curso).filter(Curso.maestro_id == id).all()
	return render_template('maestros/detallesMaes.html', id=id,nombre=nombre,apellidos=apellidos,email=email, cursos=cursos)

@maestros.route("/eliminar", methods=['GET','POST'])
def eliminar():
	create_form = forms.MaestroForm(request.form)
	if request.method == 'GET':
		id = request.args.get('id')
		# select * from maestros where matricula == id
		maes1 = db.session.query(Maestros).filter(Maestros.matricula == id).first()
		create_form.matricula.data = request.args.get('id')
		create_form.nombre.data = maes1.nombre
		create_form.apellidos.data = maes1.apellidos
		create_form.especialidad.data = maes1.especialidad
		create_form.email.data = maes1.email

	if request.method == 'POST':
		id = create_form.matricula.data
		# select * from maestros where matricula == id
		maes = Maestros.query.get(id)
		db.session.delete(maes)
		db.session.commit()
		return redirect(url_for('maestros.index'))
	return render_template("maestros/eliminarMaes.html", form=create_form)