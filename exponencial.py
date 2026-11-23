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

    total = 0
    i = 1
    for r in numeros:
        x = -1 / lam * math.log(r)
        total = total + x
        pantalla.insert("end", f"T{i} = -1/{lam:g} ln({r}) = {x:.5f} min\n")
        i = i + 1

    pantalla.insert("end", f"\nTiempo total = {total:.5f} min\n")
    pantalla.insert("end", f"Tiempo promedio = {total / len(numeros):.5f} min\n")


ventana = tk.Tk()
ventana.title("Distribución exponencial")

tk.Label(ventana, text="Lambda").grid(row=0, column=0, sticky="w", padx=5, pady=2)
lambda_campo = tk.Entry(ventana, width=10)
lambda_campo.grid(row=0, column=1, padx=5, pady=2)
lambda_campo.insert(0, "3")

tk.Label(ventana, text="Aleatorios").grid(row=1, column=0, columnspan=2)
aleatorios = tk.Text(ventana, width=22, height=8)
aleatorios.grid(row=2, column=0, columnspan=2, padx=5)
aleatorios.insert("1.0", "0.15957\n0.26340\n0.73701\n0.25332\n0.18782")

tk.Button(ventana, text="Calcular", width=20, command=boton_calcular).grid(row=3, column=0, columnspan=2, pady=10)
pantalla = scrolledtext.ScrolledText(ventana, width=70, height=12, font=("Consolas", 10))
pantalla.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

ventana.mainloop()
