# para correrlo: pip install flask  y luego  python app.py

import random
from flask import Flask, render_template, request

# el html está en la misma carpeta que este archivo
app = Flask(__name__, template_folder=".")


@app.route("/", methods=["GET", "POST"])
def inicio():

    # al abrir la página solo se muestra el formulario
    if request.method == "GET":
        return render_template("index.html")

    capital = int(request.form["capital"])
    meta = int(request.form["meta"])
    apuesta_inicial = int(request.form["apuesta"])
    limite = float(request.form["limite"])
    corridas = int(request.form["corridas"])

    if meta <= capital:
        return render_template("index.html", error="La meta tiene que ser mayor que el capital inicial.")

    filas = []
    metas = 0
    quiebras = 0

    for corrida in range(1, corridas + 1):
        dinero = capital
        apuesta = apuesta_inicial

        # se juega hasta llegar a la meta o quedarse sin dinero
        while dinero > 0 and dinero < meta:

            # si no le alcanza, apuesta todo lo que tiene
            if apuesta > dinero:
                apuesta = dinero

            antes = dinero
            aleatorio = round(random.random(), 4)

            if aleatorio <= limite:
                gano = "SÍ"
                dinero = dinero + apuesta
            else:
                gano = "NO"
                dinero = dinero - apuesta

            if dinero >= meta:
                resultado = "META"
                metas = metas + 1
            elif dinero == 0:
                resultado = "QUIEBRA"
                quiebras = quiebras + 1
            else:
                resultado = "-"

            filas.append([corrida, antes, apuesta, aleatorio, gano, dinero, resultado])

            # si gana regresa a la apuesta inicial, si pierde la duplica
            if gano == "SÍ":
                apuesta = apuesta_inicial
            else:
                apuesta = apuesta * 2

    prob_meta = round(metas / corridas * 100, 2)
    prob_quiebra = round(quiebras / corridas * 100, 2)

    return render_template("index.html", filas=filas, metas=metas, quiebras=quiebras,
                           prob_meta=prob_meta, prob_quiebra=prob_quiebra)


app.run()
