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
        numeros = leer_numeros(aleatorios.get("1.0", "end"))
        n = int(intervalos.get())
        x_tablas = float(tablas.get())
    except ValueError:
        pantalla.insert("end", "Revisa los datos: hay un valor que no es número.\n")
        return

    total = len(numeros)
    fe = total / n
    fo = [0] * n
    for r in numeros:
        intervalo = int(r * n)
        if intervalo == n:
            intervalo = n - 1
        fo[intervalo] = fo[intervalo] + 1

    suma = 0
    pantalla.insert("end", "Intervalo\t\tFE\tFO\t(FO-FE)^2\n")
    for i in range(n):
        cuadrado = (fo[i] - fe) ** 2
        suma = suma + cuadrado
        pantalla.insert("end", f"{i / n:.2f} a {(i + 1) / n:.2f}\t\t{fe:g}\t{fo[i]}\t{cuadrado:g}\n")

    x0 = suma / fe
    pantalla.insert("end", f"\nFE = N/n = {total}/{n} = {fe:g}\n")
    pantalla.insert("end", f"Xo^2 = 1/{fe:g} ({suma:g}) = {x0:.4f}\n")
    pantalla.insert("end", f"X^2 alfa,n-1 = {x_tablas}\n\n")
    if x0 < x_tablas:
        pantalla.insert("end", f"{x0:.4f} < {x_tablas}  Los números son aceptados\n")
    else:
        pantalla.insert("end", f"{x0:.4f} >= {x_tablas}  Los números son rechazados\n")


def campo(texto, valor, fila):
    tk.Label(ventana, text=texto).grid(row=fila, column=0, sticky="w", padx=5, pady=2)
    entrada = tk.Entry(ventana, width=10)
    entrada.grid(row=fila, column=1, padx=5, pady=2)
    entrada.insert(0, valor)
    return entrada


ventana = tk.Tk()
ventana.title("Prueba de frecuencias")

intervalos = campo("Intervalos (n)", "4", 0)
tablas = campo("X^2 alfa,n-1 (de tablas)", "7.81", 1)

tk.Label(ventana, text="Aleatorios").grid(row=2, column=0, columnspan=2)
aleatorios = tk.Text(ventana, width=22, height=10)
aleatorios.grid(row=3, column=0, columnspan=2, padx=5)
aleatorios.insert("1.0", "0.15021\n0.33295\n0.37509\n0.82162\n0.67946\n0.84145\n0.90279\n0.77074\n0.18002\n0.18464")

tk.Button(ventana, text="Calcular", width=20, command=boton_calcular).grid(row=4, column=0, columnspan=2, pady=10)
pantalla = scrolledtext.ScrolledText(ventana, width=80, height=15, font=("Consolas", 10))
pantalla.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

ventana.mainloop()
