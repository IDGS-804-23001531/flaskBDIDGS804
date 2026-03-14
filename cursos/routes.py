import forms
from flask import render_template, request, redirect, url_for
from models import db, Curso, Maestros, Alumnos
from . import cursos
from flask import flash
from forms import CursoForm, InscripcionForm

@cursos.route("/cursos")
@cursos.route("/index")
def index():
    create_form = forms.CursoForm(request.form)
    cursos_lista = Curso.query.all()
    return render_template("cursos/listadoCursos.html", form=create_form, cursos=cursos_lista)

@cursos.route("/nuevoCur", methods=['GET', 'POST'])
def nuevoCur():
    create_form = forms.CursoForm(request.form)
    create_form.maestro_id.choices = [
        (m.matricula, f"{m.nombre} {m.apellidos} - {m.especialidad}")
        for m in Maestros.query.all()
    ]
    if request.method == 'POST' and create_form.validate():
        nuevo_curso = Curso(
            nombre=create_form.nombre.data,
            descripcion=create_form.descripcion.data,
            maestro_id=create_form.maestro_id.data
        )
        db.session.add(nuevo_curso)
        db.session.commit()
        return redirect('/cursos')
    return render_template("cursos/Cursos.html", form=create_form)

@cursos.route("/modificarCur", methods=['GET', 'POST'])
def modificarCur():
    create_form = forms.CursoForm(request.form)
    create_form.maestro_id.choices = [
        (m.matricula, f"{m.nombre} {m.apellidos} - {m.especialidad}")
        for m in Maestros.query.all()
    ]
    if request.method == 'GET':
        id = request.args.get('id')
        curso = Curso.query.get(id)
        create_form.id.data = curso.id
        create_form.nombre.data = curso.nombre
        create_form.descripcion.data = curso.descripcion
        create_form.maestro_id.data = curso.maestro_id

    if request.method == 'POST' and create_form.validate():
        id = create_form.id.data
        curso = Curso.query.get(id)
        curso.nombre = create_form.nombre.data
        curso.descripcion = create_form.descripcion.data
        curso.maestro_id = create_form.maestro_id.data
        db.session.commit()
        return redirect('/cursos')
    return render_template("cursos/modificarCursos.html", form=create_form)

@cursos.route("/eliminarCur", methods=['GET', 'POST'])
def eliminarCur():
    create_form = forms.CursoForm(request.form)
    create_form.maestro_id.choices = [
        (m.matricula, m.nombre + " " + m.apellidos)
        for m in Maestros.query.all()
    ]
    if request.method == 'GET':
        id = request.args.get('id')
        curso = Curso.query.get(id)
        create_form.id.data = curso.id
        create_form.nombre.data = curso.nombre
        create_form.descripcion.data = curso.descripcion
        create_form.maestro_id.data = curso.maestro_id

    if request.method == 'POST':
        id = create_form.id.data
        curso = Curso.query.get(id)
        db.session.delete(curso)
        db.session.commit()
        return redirect('/cursos')
    return render_template("cursos/eliminarCursos.html", form=create_form)

@cursos.route("/detallesCur", methods=['GET', 'POST'])
def detallesCur():
    if request.method == 'GET':
        id = request.args.get('id')
        curso = Curso.query.get(id)
        nombre = curso.nombre
        descripcion = curso.descripcion
        maestro = curso.maestro.nombre + " " + curso.maestro.apellidos

    return render_template("cursos/detallesCursos.html", id=id, nombre=nombre, descripcion=descripcion, maestro=maestro)
