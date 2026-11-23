import math
import tkinter as tk
from tkinter import scrolledtext
from statistics import NormalDist


def leer_numeros(texto):
    numeros = []
    for x in texto.replace(",", " ").split():
        numeros.append(float(x))
    return numeros


def boton_calcular():
    pantalla.delete("1.0", "end")
    try:
        numeros = leer_numeros(aleatorios.get("1.0", "end"))
        alfa = float(alfa_campo.get()) / 100
    except ValueError:
        pantalla.insert("end", "Revisa los datos: hay un valor que no es número.\n")
        return

    n = len(numeros)
    suma = sum(numeros)
    promedio = suma / n
    z0 = abs((promedio - 0.5) * math.sqrt(n) / math.sqrt(1 / 12))
    z_tablas = NormalDist().inv_cdf(1 - alfa / 2)

    pantalla.insert("end", f"N = {n}\n")
    pantalla.insert("end", f"Suma = {suma:.5f}\n")
    pantalla.insert("end", f"Promedio = {promedio:.6f}\n")
    pantalla.insert("end", f"Zo = |({promedio:.6f} - 0.5)(raíz de {n}) / raíz de 1/12| = {z0:.4f}\n")
    pantalla.insert("end", f"Z alfa/2 = {z_tablas:.2f}\n\n")
    if z0 < z_tablas:
        pantalla.insert("end", f"{z0:.4f} < {z_tablas:.2f}  Los números son aceptados\n")
    else:
        pantalla.insert("end", f"{z0:.4f} >= {z_tablas:.2f}  Los números son rechazados\n")


ventana = tk.Tk()
ventana.title("Prueba de promedio")

tk.Label(ventana, text="Alfa (%)").grid(row=0, column=0, sticky="w", padx=5, pady=2)
alfa_campo = tk.Entry(ventana, width=10)
alfa_campo.grid(row=0, column=1, padx=5, pady=2)
alfa_campo.insert(0, "5")

tk.Label(ventana, text="Aleatorios").grid(row=1, column=0, columnspan=2)
aleatorios = tk.Text(ventana, width=22, height=10)
aleatorios.grid(row=2, column=0, columnspan=2, padx=5)
aleatorios.insert("1.0", "0.15021\n0.33295\n0.37509\n0.82162\n0.67946\n0.84145\n0.90279\n0.77074\n0.18002\n0.18464")

tk.Button(ventana, text="Calcular", width=20, command=boton_calcular).grid(row=3, column=0, columnspan=2, pady=10)
pantalla = scrolledtext.ScrolledText(ventana, width=80, height=15, font=("Consolas", 10))
pantalla.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

ventana.mainloop()
