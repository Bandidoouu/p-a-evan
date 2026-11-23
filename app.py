import random


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


def pedir(texto, defecto):
    dato = input(texto + " [" + defecto + "]: ")
    if dato == "":
        return defecto
    return dato


def pedir_tabla(texto, valores, probabilidades):
    print(texto)
    valores = pedir("  Valores", valores).split()
    probabilidades = pedir("  Probabilidades", probabilidades).split()
    tabla = []
    for i in range(len(valores)):
        tabla.append([int(valores[i]), float(probabilidades[i])])
    return tabla


def pedir_aleatorios(texto):
    numeros = []
    for x in input(texto + " [al azar]: ").split():
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


def simular(personas, tabla_servicio):
    filas = []

    for i in range(buscar(r_inicial, tabla_inicial)):
        filas.append({"r_llegada": "-", "entre": "-", "llegada": apertura})

    llegada = apertura
    for r in r_llegadas:
        entre = buscar(r, tabla_llegadas)
        llegada = llegada + entre
        if llegada > limite:
            break
        filas.append({"r_llegada": r, "entre": entre, "llegada": llegada})

    fin_anterior = apertura
    comieron = False
    comida = "-"

    for i in range(len(filas)):
        fila = filas[i]

        if fila["llegada"] > fin_anterior:
            inicio = fila["llegada"]
        else:
            inicio = fin_anterior
        ocio = inicio - fin_anterior

        if comieron == False and inicio >= hora_comida:
            if fin_anterior > hora_comida:
                inicio_comida = fin_anterior
            else:
                inicio_comida = hora_comida
            fin_comida = inicio_comida + minutos_comida
            if fila["llegada"] > fin_comida:
                inicio = fila["llegada"]
            else:
                inicio = fin_comida
            ocio = inicio - fin_anterior - minutos_comida
            comieron = True
            comida = a_hora(inicio_comida) + " a " + a_hora(fin_comida)

        cola = 0
        for j in range(i):
            if filas[j]["fin"] > fila["llegada"]:
                cola = cola + 1

        fila["inicio"] = inicio
        fila["r_servicio"] = r_servicio[i]
        fila["servicio"] = buscar(r_servicio[i], tabla_servicio)
        fila["fin"] = inicio + fila["servicio"]
        fila["ocio"] = ocio
        fila["espera"] = inicio - fila["llegada"]
        fila["cola"] = cola
        fin_anterior = fila["fin"]

    espera = 0
    for fila in filas:
        espera = espera + fila["espera"]

    extra = 0
    if fin_anterior > limite:
        extra = fin_anterior - limite

    horas = (limite - apertura) / 60
    resultado = {"personas": personas, "filas": filas, "comida": comida, "espera": espera}
    resultado["normal"] = personas * horas * salario
    resultado["extra"] = personas * extra / 60 * salario_extra
    resultado["costo_espera"] = espera / 60 * costo_espera
    resultado["almacen"] = (horas + extra / 60) * costo_almacen
    resultado["total"] = resultado["normal"] + resultado["extra"] + resultado["costo_espera"] + resultado["almacen"]
    return resultado


apertura = a_minutos(pedir("Hora de apertura", "23:00"))
limite = a_minutos(pedir("Hora límite de llegada", "07:30"))
hora_comida = a_minutos(pedir("Hora de comida", "03:00"))
minutos_comida = int(pedir("Minutos de comida", "30"))
if limite < apertura:
    limite = limite + 24 * 60
if hora_comida < apertura:
    hora_comida = hora_comida + 24 * 60

salario = float(pedir("Salario normal por hora", "25"))
salario_extra = float(pedir("Salario extra por hora", "37.5"))
costo_espera = float(pedir("Costo por hora de camión esperando", "100"))
costo_almacen = float(pedir("Costo por hora del almacén", "500"))

tabla_inicial = pedir_tabla("Camiones esperando al abrir", "0 1 2 3", ".50 .25 .15 .10")
tabla_llegadas = pedir_tabla("Tiempo entre llegadas", "20 25 30 35 40 45 50 55 60", ".02 .08 .12 .25 .20 .15 .10 .05 .03")

r_inicial = pedir_aleatorios("Aleatorio para camiones al abrir")[0]
r_llegadas = pedir_aleatorios("Aleatorios para llegadas")
r_servicio = pedir_aleatorios("Aleatorios para servicio")

equipos = [
    ["3", "20 25 30 35 40 45 50 55 60", ".05 .10 .20 .25 .12 .10 .08 .06 .04"],
    ["4", "15 20 25 30 35 40 45 50 55", ".05 .15 .20 .20 .15 .12 .08 .04 .01"],
    ["5", "10 15 20 25 30 35 40 45 50", ".10 .18 .22 .18 .10 .08 .06 .05 .03"],
    ["6", "5 10 15 20 25 30 35 40 45", ".12 .15 .26 .15 .12 .08 .06 .04 .02"],
]

resultados = []
for equipo in equipos:
    personas = pedir("Personas del equipo", equipo[0])
    tabla_servicio = pedir_tabla("Tiempo de servicio con " + personas + " personas", equipo[1], equipo[2])
    resultados.append(simular(int(personas), tabla_servicio))

print()
print("Aleatorio para camiones al abrir:", r_inicial)

for res in resultados:
    print()
    print("EQUIPO DE", res["personas"], "PERSONAS")
    print("Comida:", res["comida"], "   Espera total:", res["espera"], "min")
    print("#", "R lleg", "Entre", "Llega", "Inicio", "R serv", "Serv", "Fin", "Ocio", "Espera", "Cola", sep="\t")
    numero = 1
    for f in res["filas"]:
        print(numero, f["r_llegada"], f["entre"], a_hora(f["llegada"]), a_hora(f["inicio"]), f["r_servicio"], f["servicio"], a_hora(f["fin"]), f["ocio"], f["espera"], f["cola"], sep="\t")
        numero = numero + 1

print()
print("COMPARACIÓN DE COSTOS")
print("Equipo", "Normal", "Extra", "Espera", "Almacén", "Total", sep="\t")
mejor = resultados[0]
for res in resultados:
    print(res["personas"], round(res["normal"], 2), round(res["extra"], 2), round(res["costo_espera"], 2), round(res["almacen"], 2), round(res["total"], 2), sep="\t")
    if res["total"] < mejor["total"]:
        mejor = res

print()
print("Equipo óptimo:", mejor["personas"], "personas con costo de", round(mejor["total"], 2))
input()
