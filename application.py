import os
import sys
import random
from sys import argv, exit

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# # Configure application
app = Flask(__name__)


app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL("sqlite:///thoth.db")

@app.route("/", methods=["GET"])
def index():

    return render_template("index.html")




@app.route("/recursos", methods=["GET"])
def recursos():

    return render_template("recursos_lectura.html")


@app.route("/contacto", methods=["GET"])
def contacto():

    return render_template("contacto.html")

@app.route("/quienes_somos", methods=["GET"])
def quienes_somos():

    return render_template("quienes_somos.html")


categorias = ['general','avanzado']

@app.route("/evaluate", methods=["GET"])
def evaluate():

    return render_template("evaluate.html",categorias=categorias)

#Ruta que extrae y almacena en memoria las lecturas de la base de datos, segun la categoria de lecturas
#que el usuario haya escogido




@app.route("/iniciate", methods=["POST"])
def iniciate():

    #
    categoria = request.form.get("valor")




    #Ejecuta base de datos y almacena su contenido en un list dict
    lecturas = db.execute("SELECT * FROM lecturas WHERE tipo = ?", categoria)
    foo = random.choice(lecturas)

    lectura_nombre = foo['nombre']
    lectura_texto = foo['lectura']
    id_lectura = foo['lecture_id']
    session["id_lectura"] = id_lectura

    preguntas_respuestas = db.execute("SELECT * FROM preguntas_tipo_opcion WHERE lectura_id = ?", id_lectura)

    for row in preguntas_respuestas:
        headers = row.keys()
        break

    lista = []

    for key in headers:
        if key != 'lectura_id' and key != 'pregunta':
            lista.append(key)
            random.shuffle(lista)


    return render_template("prueba.html", lectura = foo, lectura_nombre = lectura_nombre, lectura_texto = lectura_texto, preguntas = preguntas_respuestas, lista = lista)


@app.route("/grade", methods=["POST"])
def grade():


    id_lectura = session.get("id_lectura",None)

    preguntas_respuestas = db.execute("SELECT * FROM preguntas_tipo_opcion WHERE lectura_id = ?", id_lectura)

    for row in preguntas_respuestas:
        headers = row.keys()
        break

    lista = []

    for key in headers:
        if key != 'lectura_id' and key != 'pregunta':
            lista.append(key)

    suma = 0
    length = 0
    for row in preguntas_respuestas:
        for key in lista:
            name = row[key]
            respuesta = request.form.get(name)
            if respuesta == row['opcion_correcta']:
                suma = suma + 1
                break
        length = length + 1

    print(suma)
    print(length)

    if length == 5:

        if suma == length:
            calificacion = '100%'

        elif suma == (0.8 * length):
            calificacion = '80%'

        elif suma == (0.6 * length):
            calificacion = '60%'

        elif suma == (0.4 * length):
            calificacion = '40%'

        elif suma == (0.2 * length):
            calificacion = '20%'

        else:
            calificacion = '0%'

    if length == 4:

        if suma == length:
            calificacion = '100%'

        elif suma == (0.75 * length):
            calificacion = '75%'

        elif suma == (0.5 * length):
            calificacion = '50%'

        elif suma == (0.25 * length):
            calificacion = '25%'

        else:
            calificacion = '0%'

    if length == 3:
        if suma == length:
            calificacion = '100%'

        elif suma == (length - 1):
            calificacion = '66%'

        elif suma == (length - 2):
            calificacion = '33%'
        else:
            calificacion = '0%'

    if length == 2:
        if suma == length:
            calificacion = '100%'
        elif suma == length - 1:
            calificacion = '50%'
        else:
            calificacion = '0%'

    return render_template("test.html", calificacion=calificacion)



