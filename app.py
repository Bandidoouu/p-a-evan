# Simulación de colas: descarga de camiones en un almacén
# para correrlo (desde esta carpeta):  python app.py
# y abrir en el navegador:  http://127.0.0.1:8000

import random
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qsl


# "23:00" -> 1380 minutos
def a_minutos(texto):
    partes = texto.split(":")
    return int(partes[0]) * 60 + int(partes[1])


# 1380 minutos -> "11:00" (formato de 12 horas, como en la libreta)
def a_hora(minutos):
    h = (minutos // 60) % 12
    if h == 0:
        h = 12
    return str(h) + ":" + str(minutos % 60).zfill(2)


# "20 0.02\n25 0.08"  ->  [[20, 0.02], [25, 0.08]]
def leer_tabla(texto):
    tabla = []
    for renglon in texto.splitlines():
        partes = renglon.split()
        if len(partes) == 2:
            tabla.append([int(partes[0]), float(partes[1])])
    return tabla


# "0.19241, 0.15997"  ->  [0.19241, 0.15997, ...]
# si no escribieron suficientes números, se completan al azar
def leer_aleatorios(texto):
    numeros = []
    for x in texto.replace(",", " ").split():
        numeros.append(float(x))
    while len(numeros) < 500:
        numeros.append(round(random.random(), 5))
    return numeros


# regla de la libreta: si R > acumulada anterior y R <= acumulada, entonces X = valor
def escoger(r, tabla):
    acumulada = 0
    for valor, prob in tabla:
        acumulada = round(acumulada + prob, 4)
        if r <= acumulada:
            return valor
    return tabla[-1][0]


# simula la noche completa con un equipo de "personas" trabajadores
# d trae todos los datos que escribió el usuario
def simular(personas, tabla_servicio, d):
    filas = []

    # 1) camiones que ya están esperando cuando abre el almacén
    iniciales = escoger(d["r_inicial"], d["tabla_inicial"])
    for i in range(iniciales):
        filas.append({"r_llegada": "-", "entre": "-", "llegada": d["apertura"]})

    # 2) llegadas: se va sumando el tiempo entre llegadas hasta pasar la hora límite
    hora = d["apertura"]
    for r in d["r_llegadas"]:
        entre = escoger(r, d["tabla_llegadas"])
        hora = hora + entre
        if hora > d["limite"]:
            break  # después de la hora límite ya no se reciben camiones
        filas.append({"r_llegada": r, "entre": entre, "llegada": hora})

    # 3) se atiende a los camiones en orden de llegada
    fin_anterior = d["apertura"]
    ya_comieron = False
    comida = "no les tocó comer"

    for i in range(len(filas)):
        fila = filas[i]
        llegada = fila["llegada"]

        # empieza cuando llega el camión o cuando se desocupan, lo que pase después
        inicio = max(llegada, fin_anterior)
        ocio = inicio - fin_anterior

        # comida: si ya es la hora de comer, primero comen y luego atienden
        # (si estaban descargando un camión a esa hora, comen al terminarlo)
        if not ya_comieron and inicio >= d["comida"]:
            inicio_comida = max(fin_anterior, d["comida"])
            fin_comida = inicio_comida + d["duracion_comida"]
            inicio = max(llegada, fin_comida)
            ocio = inicio - fin_anterior - d["duracion_comida"]
            ya_comieron = True
            comida = a_hora(inicio_comida) + " a " + a_hora(fin_comida)

        r = d["r_servicio"][i]
        servicio = escoger(r, tabla_servicio)
        fin = inicio + servicio

        # longitud de la cola: camiones anteriores que siguen en el almacén cuando llega este
        cola = 0
        for anterior in filas[:i]:
            if anterior["fin"] > llegada:
                cola = cola + 1

        fila["inicio"] = inicio
        fila["r_servicio"] = r
        fila["servicio"] = servicio
        fila["fin"] = fin
        fila["ocio"] = ocio
        fila["espera"] = inicio - llegada
        fila["cola"] = cola
        fin_anterior = fin

    # 4) costos
    espera_total = 0
    for fila in filas:
        espera_total = espera_total + fila["espera"]

    horas_normales = (d["limite"] - d["apertura"]) / 60
    horas_extra = max(0, fin_anterior - d["limite"]) / 60
    horas_almacen = (max(fin_anterior, d["limite"]) - d["apertura"]) / 60

    salario_normal = personas * horas_normales * d["salario"]
    salario_extra = personas * horas_extra * d["salario_extra"]
    costo_espera = espera_total / 60 * d["costo_espera"]
    costo_almacen = horas_almacen * d["costo_almacen"]

    return {
        "personas": personas,
        "filas": filas,
        "comida": comida,
        "espera_total": espera_total,
        "salario_normal": salario_normal,
        "salario_extra": salario_extra,
        "costo_espera": costo_espera,
        "costo_almacen": costo_almacen,
        "total": salario_normal + salario_extra + costo_espera + costo_almacen,
    }


# recibe los datos del formulario y regresa la página con los resultados
def procesar(form):

    # 1) leer los datos
    d = {}
    d["apertura"] = a_minutos(form["apertura"])
    d["limite"] = a_minutos(form["limite"])
    d["comida"] = a_minutos(form["comida"])
    # turno de noche: si una hora es menor que la de apertura, es del día siguiente
    if d["limite"] < d["apertura"]:
        d["limite"] = d["limite"] + 24 * 60
    if d["comida"] < d["apertura"]:
        d["comida"] = d["comida"] + 24 * 60
    d["duracion_comida"] = int(form["duracion_comida"])

    d["salario"] = float(form["salario"])
    d["salario_extra"] = float(form["salario_extra"])
    d["costo_espera"] = float(form["costo_espera"])
    d["costo_almacen"] = float(form["costo_almacen"])

    d["tabla_inicial"] = leer_tabla(form["inicial"])
    d["tabla_llegadas"] = leer_tabla(form["llegadas"])

    # todos los equipos usan los mismos números aleatorios, así la comparación es justa
    d["r_inicial"] = leer_aleatorios(form["r_inicial"])[0]
    d["r_llegadas"] = leer_aleatorios(form["r_llegadas"])
    d["r_servicio"] = leer_aleatorios(form["r_servicio"])

    # 2) simular cada equipo
    resultados = []
    for i in ["1", "2", "3", "4"]:
        personas = int(form["personas" + i])
        tabla_servicio = leer_tabla(form["servicio" + i])
        resultados.append(simular(personas, tabla_servicio, d))

    # el equipo óptimo es el de menor costo total
    mejor = resultados[0]
    for res in resultados:
        if res["total"] < mejor["total"]:
            mejor = res

    # 3) armar la página de resultados
    html = "<button onclick='history.back()'>Volver a los datos</button>"
    html += "<h2>Comparación de equipos</h2>"
    html += "<table border='1' cellpadding='5'>"
    html += "<tr><th>Personas</th><th>Salario normal</th><th>Tiempo extra</th><th>Espera camiones</th><th>Almacén</th><th>Costo total</th></tr>"
    for res in resultados:
        html += "<tr>"
        html += f"<td>{res['personas']}</td>"
        html += f"<td>${res['salario_normal']:.2f}</td>"
        html += f"<td>${res['salario_extra']:.2f}</td>"
        html += f"<td>${res['costo_espera']:.2f}</td>"
        html += f"<td>${res['costo_almacen']:.2f}</td>"
        html += f"<td>${res['total']:.2f}</td>"
        html += "</tr>"
    html += "</table>"
    html += f"<h2>Equipo óptimo: {mejor['personas']} personas (${mejor['total']:.2f})</h2>"
    html += f"<p>R para camiones al abrir: {d['r_inicial']}</p>"

    for res in resultados:
        html += f"<h2>Equipo de {res['personas']} personas</h2>"
        html += f"<p>Comida: {res['comida']}<br>Espera total de camiones: {res['espera_total']} min</p>"
        html += "<table border='1' cellpadding='5'>"
        html += "<tr><th>#</th><th>R llegada</th><th>Tiempo entre llegadas</th><th>Hora de llegada</th><th>Inicio servicio</th>"
        html += "<th>R servicio</th><th>Tiempo servicio</th><th>Fin servicio</th><th>Ocio personal</th><th>Espera camión</th><th>Longitud cola</th></tr>"
        numero = 1
        for f in res["filas"]:
            html += "<tr>"
            html += f"<td>{numero}</td>"
            html += f"<td>{f['r_llegada']}</td>"
            html += f"<td>{f['entre']}</td>"
            html += f"<td>{a_hora(f['llegada'])}</td>"
            html += f"<td>{a_hora(f['inicio'])}</td>"
            html += f"<td>{f['r_servicio']}</td>"
            html += f"<td>{f['servicio']}</td>"
            html += f"<td>{a_hora(f['fin'])}</td>"
            html += f"<td>{f['ocio']}</td>"
            html += f"<td>{f['espera']}</td>"
            html += f"<td>{f['cola']}</td>"
            html += "</tr>"
            numero = numero + 1
        html += "</table>"

    return html


# el servidor: cuando se abre la página manda index.html,
# y cuando se le da "Simular" recibe los datos y manda los resultados
class Servidor(BaseHTTPRequestHandler):

    def do_GET(self):
        self.mandar(open("index.html", encoding="utf-8").read())

    def do_POST(self):
        largo = int(self.headers["Content-Length"])
        texto = self.rfile.read(largo).decode("utf-8")
        form = dict(parse_qsl(texto, keep_blank_values=True))
        self.mandar(procesar(form))

    def mandar(self, html):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))


print("Abre en el navegador: http://127.0.0.1:8000")
HTTPServer(("127.0.0.1", 8000), Servidor).serve_forever()
