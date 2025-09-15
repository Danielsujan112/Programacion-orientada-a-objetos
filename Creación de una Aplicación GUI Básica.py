import tkinter as tk
from tkinter import messagebox

# -------------------------
# Aplicacion GUI con Tkinter
# -------------------------

# Funcion para agregar texto a la lista
def agregar():
    texto = entrada.get().strip()
    if texto:  # Verifica que no este vacio
        lista.insert(tk.END, texto)
        entrada.delete(0, tk.END)  # Limpiar campo de texto
    else:
        messagebox.showwarning("Advertencia", "No se puede agregar un campo vacio.")

# Funcion para limpiar elementos seleccionados o todo
def limpiar():
    seleccion = lista.curselection()
    if seleccion:  # Si hay elementos seleccionados, los elimina
        for index in reversed(seleccion):  # reversed para no alterar índices
            lista.delete(index)
    else:  # Si no hay selección, borra todo
        lista.delete(0, tk.END)

# -------------------------
# Configuración de la ventana
# -------------------------
ventana = tk.Tk()
ventana.title("Gestión de Datos con GUI")
ventana.geometry("400x300")

# -------------------------
# Componentes de la interfaz
# -------------------------

# Etiqueta
label = tk.Label(ventana, text="Ingrese información:")
label.pack(pady=5)

# Campo de texto
entrada = tk.Entry(ventana, width=40)
entrada.pack(pady=5)

# Botón Agregar
boton_agregar = tk.Button(ventana, text="Agregar", command=agregar)
boton_agregar.pack(pady=5)

# Botón Limpiar
boton_limpiar = tk.Button(ventana, text="Limpiar", command=limpiar)
boton_limpiar.pack(pady=5)

# Lista para mostrar datos
lista = tk.Listbox(ventana, width=50, height=10)
lista.pack(pady=10)

# -------------------------
# Ejecutar la aplicación
# -------------------------
ventana.mainloop()
