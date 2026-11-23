import math
import tkinter as tk
from tkinter import scrolledtext


def leer_numeros(texto):
    numeros = []
    for x in texto.replace(",", " ").split():
        numeros.append(float(x))
    return numeros


def boton_calcular():
    pantalla.delete("1.0", "end")
    try:
        lam = float(lambda_campo.get())
        numeros = leer_numeros(aleatorios.get("1.0", "end"))
    except ValueError:
        pantalla.insert("end", "Revisa los datos: hay un valor que no es número.\n")
        return

    pantalla.insert("end", "x\tf(x)\tF(x)\n")
    tabla = []
    acumulada = 0
    x = 0
    while acumulada < 0.999:
        f = round(math.exp(-lam) * lam ** x / math.factorial(x), 5)
        acumulada = round(acumulada + f, 5)
        tabla.append([x, acumulada])
        pantalla.insert("end", f"{x}\t{f:.5f}\t{acumulada:.5f}\n")
        x = x + 1
    tabla[-1][1] = 1

    pantalla.insert("end", "\nTABLA DE RANGOS\n")
    anterior = 0
    for renglon in tabla:
        pantalla.insert("end", f"Si R > {anterior:.5f} y <= {renglon[1]:.5f} entonces x = {renglon[0]}\n")
        anterior = renglon[1]

    pantalla.insert("end", "\nDía\tR\tDemanda\n")
    total = 0
    dia = 1
    for r in numeros:
        for renglon in tabla:
            if r <= renglon[1]:
                demanda = renglon[0]
                break
        total = total + demanda
        pantalla.insert("end", f"{dia}\t{r}\t{demanda}\n")
        dia = dia + 1

    pantalla.insert("end", f"\nDemanda total = {total} productos\n")


ventana = tk.Tk()
ventana.title("Distribución de Poisson")

tk.Label(ventana, text="Lambda (media)").grid(row=0, column=0, sticky="w", padx=5, pady=2)
lambda_campo = tk.Entry(ventana, width=10)
lambda_campo.grid(row=0, column=1, padx=5, pady=2)
lambda_campo.insert(0, "5")

tk.Label(ventana, text="Aleatorios (uno por día)").grid(row=1, column=0, columnspan=2)
aleatorios = tk.Text(ventana, width=22, height=8)
aleatorios.grid(row=2, column=0, columnspan=2, padx=5)
aleatorios.insert("1.0", "0.63247\n0.58789\n0.97899\n0.99542\n0.85947")

tk.Button(ventana, text="Calcular", width=20, command=boton_calcular).grid(row=3, column=0, columnspan=2, pady=10)
pantalla = scrolledtext.ScrolledText(ventana, width=70, height=25, font=("Consolas", 10))
pantalla.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

ventana.mainloop()
