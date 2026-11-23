import os
import sys
import random
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qsl


def a_minutos(texto):
    partes = texto.split(":")
    return int(partes[0]) * 60 + int(partes[1])


def a_hora(minutos):
    h = minutos // 60 % 12
    m = minutos % 60
    if h == 0:
        h = 12
    if m < 10:
        return str(h) + ":0" + str(m)
    return str(h) + ":" + str(m)


def leer_tabla(texto):
    tabla = []
    for renglon in texto.splitlines():
        partes = renglon.split()
        if len(partes) == 2:
            tabla.append([int(partes[0]), float(partes[1])])
    return tabla


def leer_aleatorios(texto):
    numeros = []
    for x in texto.replace(",", " ").split():
        numeros.append(float(x))
    while len(numeros) < 500:
        numeros.append(round(random.random(), 5))
    return numeros


def buscar(r, tabla):
    acumulada = 0
    for renglon in tabla:
        acumulada = round(acumulada + renglon[1], 4)
        if r <= acumulada:
            return renglon[0]
    return tabla[-1][0]


def simular(personas, servicio, datos):
    filas = []

    iniciales = buscar(datos["r_inicial"], datos["inicial"])
    for i in range(iniciales):
        filas.append({"r_llegada": "-", "entre": "-", "llegada": datos["apertura"]})

    llegada = datos["apertura"]
    for r in datos["r_llegadas"]:
        entre = buscar(r, datos["llegadas"])
        llegada = llegada + entre
        if llegada > datos["limite"]:
            break
        filas.append({"r_llegada": r, "entre": entre, "llegada": llegada})

    fin_anterior = datos["apertura"]
    comieron = False
    comida = "no les tocó comer"

    for i in range(len(filas)):
        fila = filas[i]

        if fila["llegada"] > fin_anterior:
            inicio = fila["llegada"]
        else:
            inicio = fin_anterior
        ocio = inicio - fin_anterior

        if comieron == False and inicio >= datos["comida"]:
            if fin_anterior > datos["comida"]:
                inicio_comida = fin_anterior
            else:
                inicio_comida = datos["comida"]
            fin_comida = inicio_comida + datos["duracion_comida"]
            if fila["llegada"] > fin_comida:
                inicio = fila["llegada"]
            else:
                inicio = fin_comida
            ocio = inicio - fin_anterior - datos["duracion_comida"]
            comieron = True
            comida = a_hora(inicio_comida) + " a " + a_hora(fin_comida)

        cola = 0
        for j in range(i):
            if filas[j]["fin"] > fila["llegada"]:
                cola = cola + 1

        r = datos["r_servicio"][i]
        fila["inicio"] = inicio
        fila["r_servicio"] = r
        fila["servicio"] = buscar(r, servicio)
        fila["fin"] = inicio + fila["servicio"]
        fila["ocio"] = ocio
        fila["espera"] = inicio - fila["llegada"]
        fila["cola"] = cola
        fin_anterior = fila["fin"]

    espera = 0
    for fila in filas:
        espera = espera + fila["espera"]

    extra = 0
    if fin_anterior > datos["limite"]:
        extra = fin_anterior - datos["limite"]

    horas = (datos["limite"] - datos["apertura"]) / 60
    resultado = {"personas": personas, "filas": filas, "comida": comida, "espera": espera}
    resultado["normal"] = personas * horas * datos["salario"]
    resultado["extra"] = personas * extra / 60 * datos["salario_extra"]
    resultado["costo_espera"] = espera / 60 * datos["costo_espera"]
    resultado["almacen"] = (horas + extra / 60) * datos["costo_almacen"]
    resultado["total"] = resultado["normal"] + resultado["extra"] + resultado["costo_espera"] + resultado["almacen"]
    return resultado


def procesar(form):
    datos = {}
    datos["apertura"] = a_minutos(form["apertura"])
    datos["limite"] = a_minutos(form["limite"])
    datos["comida"] = a_minutos(form["comida"])
    if datos["limite"] < datos["apertura"]:
        datos["limite"] = datos["limite"] + 24 * 60
    if datos["comida"] < datos["apertura"]:
        datos["comida"] = datos["comida"] + 24 * 60
    datos["duracion_comida"] = int(form["duracion_comida"])
    datos["salario"] = float(form["salario"])
    datos["salario_extra"] = float(form["salario_extra"])
    datos["costo_espera"] = float(form["costo_espera"])
    datos["costo_almacen"] = float(form["costo_almacen"])
    datos["inicial"] = leer_tabla(form["inicial"])
    datos["llegadas"] = leer_tabla(form["llegadas"])
    datos["r_inicial"] = leer_aleatorios(form["r_inicial"])[0]
    datos["r_llegadas"] = leer_aleatorios(form["r_llegadas"])
    datos["r_servicio"] = leer_aleatorios(form["r_servicio"])

    resultados = []
    for i in ["1", "2", "3", "4"]:
        resultados.append(simular(int(form["personas" + i]), leer_tabla(form["servicio" + i]), datos))

    mejor = resultados[0]
    for res in resultados:
        if res["total"] < mejor["total"]:
            mejor = res

    html = open("index.html", encoding="utf-8").read().split("<form")[0]
    html += "<p><button onclick='history.back()'>Volver a los datos</button></p>"
    html += "<div class='caja'><h2>Comparación de equipos</h2><div class='tabla'><table>"
    html += "<tr><th>Personas</th><th>Salario normal</th><th>Tiempo extra</th><th>Espera camiones</th><th>Almacén</th><th>Costo total</th></tr>"
    for res in resultados:
        if res == mejor:
            html += "<tr class='mejor'>"
        else:
            html += "<tr>"
        html += f"<td>{res['personas']}</td>"
        html += f"<td>${res['normal']:.2f}</td>"
        html += f"<td>${res['extra']:.2f}</td>"
        html += f"<td>${res['costo_espera']:.2f}</td>"
        html += f"<td>${res['almacen']:.2f}</td>"
        html += f"<td>${res['total']:.2f}</td></tr>"
    html += "</table></div>"
    html += f"<p class='optimo'>Equipo óptimo: {mejor['personas']} personas (${mejor['total']:.2f})</p>"
    html += f"<p class='nota'>R para camiones al abrir: {datos['r_inicial']}</p></div>"

    for res in resultados:
        html += f"<div class='caja'><h2>Equipo de {res['personas']} personas</h2>"
        html += f"<p class='nota'>Comida: {res['comida']} &nbsp;|&nbsp; Espera total de camiones: {res['espera']} min</p>"
        html += "<div class='tabla'><table><tr><th>#</th><th>R llegada</th><th>Tiempo entre llegadas</th><th>Hora de llegada</th><th>Inicio servicio</th>"
        html += "<th>R servicio</th><th>Tiempo servicio</th><th>Fin servicio</th><th>Ocio personal</th><th>Espera camión</th><th>Longitud cola</th></tr>"
        numero = 1
        for f in res["filas"]:
            html += f"<tr><td>{numero}</td><td>{f['r_llegada']}</td><td>{f['entre']}</td><td>{a_hora(f['llegada'])}</td>"
            html += f"<td>{a_hora(f['inicio'])}</td><td>{f['r_servicio']}</td><td>{f['servicio']}</td><td>{a_hora(f['fin'])}</td>"
            html += f"<td>{f['ocio']}</td><td>{f['espera']}</td><td>{f['cola']}</td></tr>"
            numero = numero + 1
        html += "</table></div></div>"

    html += "</main></body></html>"
    return html


class Servidor(BaseHTTPRequestHandler):

    def do_GET(self):
        self.responder(open("index.html", encoding="utf-8").read())

    def do_POST(self):
        largo = int(self.headers["Content-Length"])
        form = dict(parse_qsl(self.rfile.read(largo).decode("utf-8"), keep_blank_values=True))
        self.responder(procesar(form))

    def responder(self, html):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))


os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
servidor = HTTPServer(("127.0.0.1", 0), Servidor)
direccion = "http://127.0.0.1:" + str(servidor.server_port)
print("Simulación abierta en " + direccion)
print("No cierres esta ventana mientras la usas")
webbrowser.open(direccion)
servidor.serve_forever()
