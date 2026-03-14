from flask import Flask, render_template, request,redirect,url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask_migrate import Migrate
from flask import g
from alumnos import alumnos
from maestros import maestros
from cursos import cursos
from inscribir import inscribir
import forms
from models import db
from models import Alumnos, Maestros, Curso, Inscripcion

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(alumnos)
app.register_blueprint(maestros)
app.register_blueprint(cursos)
app.register_blueprint(inscribir)
db.init_app(app)
migrate=Migrate(app,db)
csrf=CSRFProtect()

@app.errorhandler(404)
def page_not_fount(e):
	return render_template("404.html"),404

@app.route("/")
def inicio():
    return render_template("bienvenida.html")

if __name__ == '__main__':
	csrf.init_app(app)
	
	with app.app_context():
		db.create_all()
	
	app.run(debug=True)
