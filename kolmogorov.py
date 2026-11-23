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
        numeros = sorted(leer_numeros(aleatorios.get("1.0", "end")))
        d_tablas = float(tablas.get())
    except ValueError:
        pantalla.insert("end", "Revisa los datos: hay un valor que no es número.\n")
        return

    n = len(numeros)
    dn = 0
    pantalla.insert("end", "i\txi\tF(xi)=i/n\t|F(xi)-xi|\n")
    for i in range(1, n + 1):
        xi = numeros[i - 1]
        f = i / n
        d = abs(f - xi)
        if d > dn:
            dn = d
        pantalla.insert("end", f"{i}\t{xi:.5f}\t{i}/{n} = {f:g}\t{d:.5f}\n")

    pantalla.insert("end", f"\nDn = {dn:.5f}\n")
    pantalla.insert("end", f"d alfa,N = {d_tablas}\n\n")
    if dn < d_tablas:
        pantalla.insert("end", f"{dn:.5f} < {d_tablas}  Los números son aceptados\n")
    else:
        pantalla.insert("end", f"{dn:.5f} >= {d_tablas}  Los números son rechazados\n")


ventana = tk.Tk()
ventana.title("Prueba de Kolmogorov-Smirnov")

tk.Label(ventana, text="d alfa,N (de tablas)").grid(row=0, column=0, sticky="w", padx=5, pady=2)
tablas = tk.Entry(ventana, width=10)
tablas.grid(row=0, column=1, padx=5, pady=2)
tablas.insert(0, "0.409")

tk.Label(ventana, text="Aleatorios").grid(row=1, column=0, columnspan=2)
aleatorios = tk.Text(ventana, width=22, height=10)
aleatorios.grid(row=2, column=0, columnspan=2, padx=5)
aleatorios.insert("1.0", "0.15021\n0.33295\n0.37509\n0.82162\n0.67946\n0.84145\n0.90279\n0.77074\n0.18002\n0.18464")

tk.Button(ventana, text="Calcular", width=20, command=boton_calcular).grid(row=3, column=0, columnspan=2, pady=10)
pantalla = scrolledtext.ScrolledText(ventana, width=80, height=18, font=("Consolas", 10))
pantalla.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

ventana.mainloop()
