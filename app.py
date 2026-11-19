# =============================================================
#  SIMULACIÓN DE VOLADOS (APUESTAS)
#  Regla: si pierdes, duplicas la apuesta.
#         si ganas, regresas a la apuesta inicial.
#
#  Cómo correrlo:
#    1. Instalar Flask (solo una vez):   pip install flask
#    2. Correr el programa:              python app.py
#    3. Abrir en el navegador:           http://127.0.0.1:5000
# =============================================================

import random                                      # para generar números aleatorios
from flask import Flask, render_template, request  # para hacer la página web

# Creamos la aplicación web.
# template_folder="." significa que el HTML está en esta misma carpeta.
app = Flask(__name__, template_folder=".")


# Esto se ejecuta cada vez que alguien abre la página
# o presiona el botón "Simular".
@app.route("/", methods=["GET", "POST"])
def inicio():

    # Si el usuario apenas abrió la página (todavía no presiona el botón),
    # mostramos el formulario con unos datos de ejemplo.
    if request.method == "GET":
        datos = {"capital": 50, "meta": 80, "apuesta": 10, "limite": 0.5, "corridas": 4}
        return render_template("index.html", datos=datos)

    # ---------------------------------------------------------
    # 1. LEER LOS DATOS QUE ESCRIBIÓ EL USUARIO
    # ---------------------------------------------------------
    capital = int(request.form["capital"])          # dinero con el que empieza
    meta = int(request.form["meta"])                # dinero al que quiere llegar
    apuesta_inicial = int(request.form["apuesta"])  # primera apuesta
    limite = float(request.form["limite"])          # si el aleatorio es <= a esto, gana
    corridas = int(request.form["corridas"])        # cuántas veces se repite el juego

    # Si la meta no es mayor que el capital, no hay nada que simular
    if meta <= capital:
        return render_template("index.html", datos=request.form,
                               error="La meta tiene que ser mayor que el capital inicial.")

    # ---------------------------------------------------------
    # 2. PREPARAR DÓNDE GUARDAMOS LOS RESULTADOS
    # ---------------------------------------------------------
    filas = []      # aquí se guarda cada volado para mostrarlo en la tabla
    metas = 0       # cuántas corridas llegaron a la meta
    quiebras = 0    # cuántas corridas terminaron sin dinero

    # ---------------------------------------------------------
    # 3. HACER LAS CORRIDAS
    # ---------------------------------------------------------
    for corrida in range(1, corridas + 1):

        # Al empezar cada corrida, el jugador tiene su capital inicial
        dinero = capital
        apuesta = apuesta_inicial

        # Echamos volados mientras tenga dinero y no haya llegado a la meta
        while dinero > 0 and dinero < meta:

            # Si no le alcanza para la apuesta, apuesta todo lo que tiene
            if apuesta > dinero:
                apuesta = dinero

            antes = dinero                          # dinero antes del volado
            aleatorio = round(random.random(), 4)   # número aleatorio entre 0 y 1

            # ¿Ganó o perdió?
            if aleatorio <= limite:
                gano = "SÍ"
                dinero = dinero + apuesta
            else:
                gano = "NO"
                dinero = dinero - apuesta

            # ¿Ya terminó la corrida?
            if dinero >= meta:
                resultado = "META"
                metas = metas + 1
            elif dinero == 0:
                resultado = "QUIEBRA"
                quiebras = quiebras + 1
            else:
                resultado = "-"

            # Guardamos este volado como una fila de la tabla
            filas.append([corrida, antes, apuesta, aleatorio, gano, dinero, resultado])

            # Calculamos la apuesta del siguiente volado
            if gano == "SÍ":
                apuesta = apuesta_inicial   # si ganó, regresa a la apuesta inicial
            else:
                apuesta = apuesta * 2       # si perdió, duplica la apuesta

    # ---------------------------------------------------------
    # 4. CALCULAR LAS PROBABILIDADES
    # ---------------------------------------------------------
    prob_meta = round(metas / corridas * 100, 2)
    prob_quiebra = round(quiebras / corridas * 100, 2)

    # Mandamos todo al HTML para que lo muestre
    return render_template("index.html", datos=request.form, filas=filas,
                           metas=metas, quiebras=quiebras,
                           prob_meta=prob_meta, prob_quiebra=prob_quiebra)


# Encender la página web
app.run()
