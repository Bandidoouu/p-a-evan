import tkinter as tk
from tkinter import scrolledtext


def boton_calcular():
    pantalla.delete("1.0", "end")
    try:
        x = int(semilla.get())
        a = int(multiplicador.get())
        m = int(modulo.get())
    except ValueError:
        pantalla.insert("end", "Revisa los datos: hay un valor que no es número.\n")
        return

    pantalla.insert("end", "i\tXo\t(aXo) mod m\tXn+1\tRectangular\n")
    vistos = []
    i = 1
    while x not in vistos:
        vistos.append(x)
        operacion = a * x
        siguiente = operacion % m
        pantalla.insert("end", f"{i}\t{x}\t{operacion // m} + {siguiente}/{m}\t{siguiente}\t{siguiente}/{m} = {siguiente / m:.5f}\n")
        x = siguiente
        i = i + 1

    periodo = len(vistos) - vistos.index(x)
    esperado = m / 4
    pantalla.insert("end", f"\nPeriodo = {periodo}    Periodo esperado = m/4 = {esperado:g}\n")
    if periodo == esperado:
        pantalla.insert("end", "Generador congruencial multiplicativo confiable (periodo completo)\n")
    else:
        pantalla.insert("end", "Generador congruencial multiplicativo no confiable (periodo incompleto)\n")


def campo(texto, valor, fila):
    tk.Label(ventana, text=texto).grid(row=fila, column=0, sticky="w", padx=5, pady=2)
    entrada = tk.Entry(ventana, width=10)
    entrada.grid(row=fila, column=1, padx=5, pady=2)
    entrada.insert(0, valor)
    return entrada


ventana = tk.Tk()
ventana.title("Congruencial multiplicativo")

semilla = campo("Semilla (Xo)", "5", 0)
multiplicador = campo("Multiplicador (a)", "5", 1)
modulo = campo("Módulo (m)", "32", 2)

tk.Button(ventana, text="Calcular", width=20, command=boton_calcular).grid(row=3, column=0, columnspan=2, pady=10)
pantalla = scrolledtext.ScrolledText(ventana, width=80, height=25, font=("Consolas", 10))
pantalla.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

ventana.mainloop()
