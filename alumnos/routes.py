from flask import render_template, request, redirect, url_for
from models import db, Alumnos
import forms
from . import alumnos


@alumnos.route("/alumnos", methods=['GET','POST'])
@alumnos.route("/index")
def index():
	create_form = forms.UserForm(request.form)
	alumno = Alumnos.query.all()
	return render_template("alumnos/index.html", form=create_form, alumno=alumno)


@alumnos.route("/nuevoAlu", methods=['GET','POST'])
def nuevoAlu():

    create_form = forms.UserForm(request.form)

    if request.method == 'POST':

        if create_form.validate():

            alum = Alumnos(
                nombre=create_form.nombre.data,
                apellidos=create_form.apellidos.data,
                email=create_form.email.data,
                telefono=create_form.telefono.data
            )

            db.session.add(alum)
            db.session.commit()

            return redirect(url_for('alumnos.index'))

        else:
            print(create_form.errors)  # Para ver errores en consola

    return render_template("alumnos/Alumnos.html", form=create_form)



@alumnos.route("/modificarAlu", methods=['GET','POST'])
def modificarAlu():
	create_form = forms.UserForm(request.form)

	if request.method == 'GET':
		id = request.args.get('id')
		alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
		create_form.id.data = request.args.get('id')
		create_form.nombre.data = alum1.nombre
		create_form.apellidos.data = alum1.apellidos
		create_form.email.data = alum1.email
		create_form.telefono.data = alum1.telefono

	if request.method == 'POST' and create_form.validate():
		id = create_form.id.data
		alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()

		alum1.id = id
		alum1.nombre = create_form.nombre.data
		alum1.apellidos = create_form.apellidos.data
		alum1.email = create_form.email.data
		alum1.telefono = create_form.telefono.data

		db.session.commit()
		return redirect(url_for('alumnos.index'))

	return render_template("alumnos/modificar.html", form=create_form)

@alumnos.route("/eliminarAlu", methods=['GET','POST'])
def eliminarAlu():
	create_form = forms.UserForm(request.form)
	if request.method == 'GET':
		id = request.args.get('id')
		alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
		create_form.id.data = request.args.get('id')
		create_form.nombre.data = alum1.nombre
		create_form.apellidos.data = alum1.apellidos
		create_form.email.data = alum1.email
		create_form.telefono.data = alum1.telefono
	
	if request.method == 'POST':
		id = create_form.id.data
		alum = Alumnos.query.get(id)
		db.session.delete(alum)
		db.session.commit()
		return redirect(url_for('alumnos.index'))

	return render_template("alumnos/eliminar.html", form=create_form)

@alumnos.route("/detallesAlu", methods=['GET','POST'])
def detallesAlu():
	create_form = forms.UserForm(request.form)
	if request.method == 'GET':
		id = request.args.get('id')
		alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
		id = request.args.get('id')
		nombre = alum1.nombre
		apellidos = alum1.apellidos
		email = alum1.email
		telefono = alum1.telefono
	return render_template("alumnos/detalles.html", id=id, nombre=nombre, apellidos=apellidos, email=email, telefono=telefono, alumno=alum1)