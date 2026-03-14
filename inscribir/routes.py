from . import inscribir
from flask import render_template, request, redirect, url_for
from models import Inscripcion, Alumnos, Curso, Maestros
from forms import InscripcionForm
from models import db


# PAGINA PRINCIPAL
@inscribir.route("/inscribir")
@inscribir.route("/index")
def index():

    return render_template("inscribir/inscribir.html")


# FORMULARIO INSCRIPCION
@inscribir.route("/nueva", methods=['GET','POST'])
def nueva():

    form = InscripcionForm(request.form)

    alumnos = Alumnos.query.all()
    cursos = Curso.query.all()

    form.alumno_id.choices = [
        (a.id, a.nombre + " " + a.apellidos)
        for a in alumnos
    ]

    form.curso_id.choices = [
        (c.id, c.nombre + " - " + c.maestro.nombre + " " + c.maestro.apellidos)
        for c in cursos
    ]

    if request.method == "POST" and form.validate():

        nueva = Inscripcion(
            alumno_id=form.alumno_id.data,
            curso_id=form.curso_id.data
        )

        db.session.add(nueva)
        db.session.commit()

        return redirect("/inscribir")

    return render_template(
        "inscribir/nueva.html",
        form=form
    )


# CONSULTAR INSCRIPCIONES
@inscribir.route("/consultar", methods=["GET","POST"])
def consultar():

    alumnos = Alumnos.query.all()
    maestros = Maestros.query.all()
    cursos = Curso.query.all()

    alumno_id = request.form.get("alumno_id")
    maestro_id = request.form.get("maestro_id")
    curso_id = request.form.get("curso_id")

    inscripciones = []

    if alumno_id:

        inscripciones = db.session.query(
            Alumnos.nombre,
            Alumnos.apellidos,
            Curso.nombre.label("curso"),
            Maestros.nombre.label("maestro"),
            Maestros.especialidad
        ).join(
            Inscripcion, Inscripcion.alumno_id == Alumnos.id
        ).join(
            Curso, Inscripcion.curso_id == Curso.id
        ).join(
            Maestros, Curso.maestro_id == Maestros.matricula
        ).filter(
            Alumnos.id == alumno_id
        ).all()

    elif maestro_id:

        inscripciones = db.session.query(
            Alumnos.nombre,
            Alumnos.apellidos,
            Curso.nombre.label("curso"),
            Maestros.nombre.label("maestro"),
            Maestros.especialidad
        ).join(
            Inscripcion, Inscripcion.alumno_id == Alumnos.id
        ).join(
            Curso, Inscripcion.curso_id == Curso.id
        ).join(
            Maestros, Curso.maestro_id == Maestros.matricula
        ).filter(
            Maestros.matricula == maestro_id
        ).all()

    elif curso_id:

        inscripciones = db.session.query(
            Alumnos.nombre,
            Alumnos.apellidos,
            Curso.nombre.label("curso"),
            Maestros.nombre.label("maestro"),
            Maestros.especialidad
        ).join(
            Inscripcion, Inscripcion.alumno_id == Alumnos.id
        ).join(
            Curso, Inscripcion.curso_id == Curso.id
        ).join(
            Maestros, Curso.maestro_id == Maestros.matricula
        ).filter(
            Curso.id == curso_id
        ).all()

    return render_template(
        "inscribir/consultar.html",
        alumnos=alumnos,
        maestros=maestros,
        cursos=cursos,
        inscripciones=inscripciones
    )
