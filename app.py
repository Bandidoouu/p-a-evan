import tkinter as tk
from tkinter import scrolledtext


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
    for renglon in texto.split("\n"):
        partes = renglon.split()
        if len(partes) == 2:
            tabla.append([int(partes[0]), float(partes[1])])
    return tabla


def congruencial(semilla, a, c, m, cantidad):
    numeros = []
    x = semilla
    for i in range(cantidad):
        x = (a * x + c) % m
        numeros.append(round(x / m, 5))
    return numeros


def buscar(r, tabla):
    acumulada = 0
    for renglon in tabla:
        acumulada = round(acumulada + renglon[1], 4)
        if r <= acumulada:
            return renglon[0]


def simular(personas, tabla_servicio, datos):
    filas = []

    for i in range(buscar(datos["r_inicial"], datos["inicial"])):
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
    comida = "-"

    for i in range(len(filas)):
        fila = filas[i]

        if fila["llegada"] > fin_anterior:
            inicio = fila["llegada"]
        else:
            inicio = fin_anterior
        ocio = inicio - fin_anterior

        if comieron == False and inicio >= datos["hora_comida"]:
            if fin_anterior > datos["hora_comida"]:
                inicio_comida = fin_anterior
            else:
                inicio_comida = datos["hora_comida"]
            fin_comida = inicio_comida + datos["minutos_comida"]
            if fila["llegada"] > fin_comida:
                inicio = fila["llegada"]
            else:
                inicio = fin_comida
            ocio = inicio - fin_anterior - datos["minutos_comida"]
            comieron = True
            comida = a_hora(inicio_comida) + " a " + a_hora(fin_comida)

        cola = 0
        for j in range(i):
            if filas[j]["fin"] > fila["llegada"]:
                cola = cola + 1

        fila["inicio"] = inicio
        fila["r_servicio"] = datos["r_servicio"][i]
        fila["servicio"] = buscar(datos["r_servicio"][i], tabla_servicio)
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


def boton_simular():
    datos = {}
    datos["apertura"] = a_minutos(apertura.get())
    datos["limite"] = a_minutos(limite.get())
    datos["hora_comida"] = a_minutos(hora_comida.get())
    if datos["limite"] < datos["apertura"]:
        datos["limite"] = datos["limite"] + 24 * 60
    if datos["hora_comida"] < datos["apertura"]:
        datos["hora_comida"] = datos["hora_comida"] + 24 * 60
    datos["minutos_comida"] = int(minutos_comida.get())
    datos["salario"] = float(salario.get())
    datos["salario_extra"] = float(salario_extra.get())
    datos["costo_espera"] = float(costo_espera.get())
    datos["costo_almacen"] = float(costo_almacen.get())
    datos["inicial"] = leer_tabla(inicial.get("1.0", "end"))
    datos["llegadas"] = leer_tabla(llegadas.get("1.0", "end"))
    numeros = congruencial(int(semilla.get()), int(multiplicador.get()), int(incremento.get()), int(modulo.get()), 200)
    datos["r_inicial"] = numeros[0]
    datos["r_llegadas"] = numeros[1:100]
    datos["r_servicio"] = numeros[100:]

    resultados = []
    for equipo in equipos:
        resultados.append(simular(int(equipo[0].get()), leer_tabla(equipo[1].get("1.0", "end")), datos))

    mejor = resultados[0]
    for res in resultados:
        if res["total"] < mejor["total"]:
            mejor = res

    salida = "COMPARACIÓN DE COSTOS\n"
    salida += "Equipo\tNormal\tExtra\tEspera\tAlmacén\tTotal\n"
    for res in resultados:
        salida += f"{res['personas']}\t{res['normal']:.2f}\t{res['extra']:.2f}\t{res['costo_espera']:.2f}\t{res['almacen']:.2f}\t{res['total']:.2f}\n"
    salida += f"\nEquipo óptimo: {mejor['personas']} personas con costo de ${mejor['total']:.2f}\n"
    salida += f"Aleatorio para camiones al abrir: {datos['r_inicial']}\n"

    for res in resultados:
        salida += f"\nEQUIPO DE {res['personas']} PERSONAS\n"
        salida += f"Comida: {res['comida']}    Espera total: {res['espera']} min\n"
        salida += "#\tR lleg\tEntre\tLlega\tInicio\tR serv\tServ\tFin\tOcio\tEspera\tCola\n"
        numero = 1
        for f in res["filas"]:
            salida += f"{numero}\t{f['r_llegada']}\t{f['entre']}\t{a_hora(f['llegada'])}\t{a_hora(f['inicio'])}\t"
            salida += f"{f['r_servicio']}\t{f['servicio']}\t{a_hora(f['fin'])}\t{f['ocio']}\t{f['espera']}\t{f['cola']}\n"
            numero = numero + 1

    pantalla.delete("1.0", "end")
    pantalla.insert("1.0", salida)


def campo(texto, valor, fila, columna):
    tk.Label(ventana, text=texto).grid(row=fila, column=columna, sticky="w", padx=5, pady=2)
    entrada = tk.Entry(ventana, width=35)
    entrada.insert(0, valor)
    entrada.grid(row=fila, column=columna + 1, padx=5, pady=2)
    return entrada


def cuadro(texto, valor, columna):
    tk.Label(ventana, text=texto).grid(row=0, column=columna, padx=5)
    caja = tk.Text(ventana, width=10, height=10)
    caja.insert("1.0", valor)
    caja.grid(row=1, column=columna, rowspan=14, padx=5, sticky="n")
    return caja


ventana = tk.Tk()
ventana.title("Simulación de colas")

apertura = campo("Hora de apertura", "23:00", 0, 0)
limite = campo("Hora límite de llegada", "07:30", 1, 0)
hora_comida = campo("Hora de comida", "03:00", 2, 0)
minutos_comida = campo("Minutos de comida", "30", 3, 0)
salario = campo("Salario normal por hora", "25", 4, 0)
salario_extra = campo("Salario extra por hora", "37.5", 5, 0)
costo_espera = campo("Costo por hora de camión esperando", "100", 6, 0)
costo_almacen = campo("Costo por hora del almacén", "500", 7, 0)
personas1 = campo("Personas equipo 1", "3", 8, 0)
personas2 = campo("Personas equipo 2", "4", 9, 0)
personas3 = campo("Personas equipo 3", "5", 10, 0)
personas4 = campo("Personas equipo 4", "6", 11, 0)
semilla = campo("Semilla (X0)", "12345", 12, 0)
multiplicador = campo("Multiplicador (a)", "1021", 13, 0)
incremento = campo("Incremento (c)", "7", 14, 0)
modulo = campo("Módulo (m)", "100000", 15, 0)

inicial = cuadro("Camiones al abrir", "0 .50\n1 .25\n2 .15\n3 .10", 2)
llegadas = cuadro("Entre llegadas", "20 .02\n25 .08\n30 .12\n35 .25\n40 .20\n45 .15\n50 .10\n55 .05\n60 .03", 3)
servicio1 = cuadro("Servicio equipo 1", "20 .05\n25 .10\n30 .20\n35 .25\n40 .12\n45 .10\n50 .08\n55 .06\n60 .04", 4)
servicio2 = cuadro("Servicio equipo 2", "15 .05\n20 .15\n25 .20\n30 .20\n35 .15\n40 .12\n45 .08\n50 .04\n55 .01", 5)
servicio3 = cuadro("Servicio equipo 3", "10 .10\n15 .18\n20 .22\n25 .18\n30 .10\n35 .08\n40 .06\n45 .05\n50 .03", 6)
servicio4 = cuadro("Servicio equipo 4", "5 .12\n10 .15\n15 .26\n20 .15\n25 .12\n30 .08\n35 .06\n40 .04\n45 .02", 7)

equipos = [[personas1, servicio1], [personas2, servicio2], [personas3, servicio3], [personas4, servicio4]]

tk.Button(ventana, text="Simular", width=20, command=boton_simular).grid(row=16, column=0, columnspan=8, pady=8)
pantalla = scrolledtext.ScrolledText(ventana, height=18, font=("Consolas", 10))
pantalla.grid(row=17, column=0, columnspan=8, padx=5, pady=5, sticky="we")

ventana.mainloop()
