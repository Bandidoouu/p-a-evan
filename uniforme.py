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
        a = float(minimo.get())
        b = float(maximo.get())
        numeros = leer_numeros(aleatorios.get("1.0", "end"))
    except ValueError:
        pantalla.insert("end", "Revisa los datos: hay un valor que no es número.\n")
        return

    total = 0
    i = 1
    for r in numeros:
        x = a + (b - a) * r
        total = total + x
        pantalla.insert("end", f"T{i} = {a:g} + ({b:g} - {a:g})({r}) = {x:.5f} min\n")
        i = i + 1

    pantalla.insert("end", f"\nTiempo total = {total:.5f} min\n")
    pantalla.insert("end", f"Tiempo promedio = {total / len(numeros):.5f} min\n")


def campo(texto, valor, fila):
    tk.Label(ventana, text=texto).grid(row=fila, column=0, sticky="w", padx=5, pady=2)
    entrada = tk.Entry(ventana, width=10)
    entrada.grid(row=fila, column=1, padx=5, pady=2)
    entrada.insert(0, valor)
    return entrada


ventana = tk.Tk()
ventana.title("Distribución uniforme")

minimo = campo("a (min)", "2", 0)
maximo = campo("b (min)", "4", 1)

tk.Label(ventana, text="Aleatorios").grid(row=2, column=0, columnspan=2)
aleatorios = tk.Text(ventana, width=22, height=8)
aleatorios.grid(row=3, column=0, columnspan=2, padx=5)
aleatorios.insert("1.0", "0.15957\n0.26340\n0.73701\n0.25332\n0.18782")

tk.Button(ventana, text="Calcular", width=20, command=boton_calcular).grid(row=4, column=0, columnspan=2, pady=10)
pantalla = scrolledtext.ScrolledText(ventana, width=70, height=12, font=("Consolas", 10))
pantalla.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

ventana.mainloop()
