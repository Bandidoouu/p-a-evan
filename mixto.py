import tkinter as tk
from tkinter import scrolledtext


def boton_calcular():
    pantalla.delete("1.0", "end")
    try:
        x = int(semilla.get())
        a = int(multiplicador.get())
        c = int(incremento.get())
        m = int(modulo.get())
    except ValueError:
        pantalla.insert("end", "Revisa los datos: hay un valor que no es número.\n")
        return

    pantalla.insert("end", "i\tXo\t(aXo+c) mod m\tXn+1\tRectangular\n")
    vistos = []
    i = 1
    while x not in vistos:
        vistos.append(x)
        operacion = a * x + c
        siguiente = operacion % m
        pantalla.insert("end", f"{i}\t{x}\t{operacion // m} + {siguiente}/{m}\t\t{siguiente}\t{siguiente}/{m} = {siguiente / m:.5f}\n")
        x = siguiente
        i = i + 1

    periodo = len(vistos) - vistos.index(x)
    pantalla.insert("end", f"\nPeriodo = {periodo}    m = {m}\n")
    if periodo == m:
        pantalla.insert("end", "Generador congruencial mixto confiable (periodo completo)\n")
    else:
        pantalla.insert("end", "Generador congruencial mixto no confiable (periodo incompleto)\n")


def campo(texto, valor, fila):
    tk.Label(ventana, text=texto).grid(row=fila, column=0, sticky="w", padx=5, pady=2)
    entrada = tk.Entry(ventana, width=10)
    entrada.grid(row=fila, column=1, padx=5, pady=2)
    entrada.insert(0, valor)
    return entrada


ventana = tk.Tk()
ventana.title("Congruencial mixto")

semilla = campo("Semilla (Xo)", "4", 0)
multiplicador = campo("Multiplicador (a)", "5", 1)
incremento = campo("Incremento (c)", "7", 2)
modulo = campo("Módulo (m)", "8", 3)

tk.Button(ventana, text="Calcular", width=20, command=boton_calcular).grid(row=4, column=0, columnspan=2, pady=10)
pantalla = scrolledtext.ScrolledText(ventana, width=80, height=25, font=("Consolas", 10))
pantalla.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

ventana.mainloop()
