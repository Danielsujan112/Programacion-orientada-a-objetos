"""
Agenda personal simple con Tkinter

Requisitos cubiertos:
- Ventana principal con Treeview que muestra fecha, hora y descripcion.
- Entradas para fecha, hora y descripcion.
- Botones: Agregar Evento, Eliminar Evento Seleccionado, Salir.
- DatePicker con tkcalendar (si esta instalado), fallback a Entry.
- Confirmacion al eliminar un evento.
- Organizacion con Frames.
- Comentarios explicativos.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Intentamos usar DateEntry de tkcalendar para un DatePicker agradable.
# Si no esta disponible, usamos un Entry simple y validacion basica.
try:
    from tkcalendar import DateEntry
    TKCALENDAR_AVAILABLE = True
except Exception:
    DateEntry = None
    TKCALENDAR_AVAILABLE = False


class AgendaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Agenda Personal")
        self.geometry("700x450")
        self.resizable(False, False)

        # Contenedor principal
        self.container = ttk.Frame(self, padding=10)
        self.container.pack(fill="both", expand=True)

        # Frames para organizar la GUI
        self._create_frames()
        self._create_widgets()
        self._configure_treeview()

        # Contador de IDs para elementos del Treeview (si no guardamos persistentemente)
        self._next_id = 1

    def _create_frames(self):
        """Crea los frames que organizan la ventana."""
        self.frame_list = ttk.LabelFrame(self.container, text="Eventos programados", padding=8)
        self.frame_list.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 10))

        self.frame_entry = ttk.LabelFrame(self.container, text="Agregar nuevo evento", padding=8)
        self.frame_entry.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        self.frame_actions = ttk.Frame(self.container, padding=8)
        self.frame_actions.grid(row=1, column=1, sticky="nsew")

        # Configurar expansion de columnas/filas (para buena disposicion)
        self.container.columnconfigure(0, weight=3)
        self.container.columnconfigure(1, weight=1)
        self.container.rowconfigure(0, weight=3)
        self.container.rowconfigure(1, weight=0)

    def _create_widgets(self):
        """Crea widgets: Treeview, entradas y botones."""
        # --- Treeview (lista de eventos) ---
        columns = ("fecha", "hora", "descripcion")
        self.tree = ttk.Treeview(self.frame_list, columns=columns, show="headings", height=10)
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("hora", text="Hora")
        self.tree.heading("descripcion", text="Descripcion")
        self.tree.column("fecha", width=120, anchor="center")
        self.tree.column("hora", width=80, anchor="center")
        self.tree.column("descripcion", width=420, anchor="w")

        # Scrollbar vertical
        vsb = ttk.Scrollbar(self.frame_list, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns", padx=(5,0))
        self.frame_list.columnconfigure(0, weight=1)
        self.frame_list.rowconfigure(0, weight=1)

        # --- Entradas para fecha, hora y descripcion ---
        # Fecha
        lbl_fecha = ttk.Label(self.frame_entry, text="Fecha:")
        lbl_fecha.grid(row=0, column=0, sticky="w", pady=(0, 6))
        if TKCALENDAR_AVAILABLE:
            # DateEntry de tkcalendar (interfaz tipo DatePicker)
            self.entry_fecha = DateEntry(self.frame_entry, width=14, date_pattern="yyyy-mm-dd")
        else:
            # Fallback: Entry con texto de ayuda (YYYY-MM-DD)
            self.entry_fecha = ttk.Entry(self.frame_entry)
            self.entry_fecha.insert(0, "YYYY-MM-DD")  # placeholder
            # Al hacer foco, borramos el placeholder si aun esta alli
            self.entry_fecha.bind("<FocusIn>", self._clear_placeholder_fecha)
        self.entry_fecha.grid(row=1, column=0, sticky="w", pady=(0, 8))

        # Hora
        lbl_hora = ttk.Label(self.frame_entry, text="Hora (HH:MM):")
        lbl_hora.grid(row=0, column=1, sticky="w", padx=(10, 0), pady=(0, 6))
        self.entry_hora = ttk.Entry(self.frame_entry, width=12)
        self.entry_hora.insert(0, "09:00")
        self.entry_hora.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=(0, 8))

        # Descripción (Entry amplio)
        lbl_desc = ttk.Label(self.frame_entry, text="Descripción:")
        lbl_desc.grid(row=2, column=0, sticky="w", pady=(4, 6))
        self.entry_desc = ttk.Entry(self.frame_entry, width=60)
        self.entry_desc.grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 8))

        # Botón para agregar evento (en frame_entry)
        btn_add = ttk.Button(self.frame_entry, text="Agregar Evento", command=self.agregar_evento)
        btn_add.grid(row=4, column=0, sticky="w", pady=(6,0))

        # --- Botones de acciones (Eliminar, Salir) ---
        btn_delete = ttk.Button(self.frame_actions, text="Eliminar Evento Seleccionado", command=self.eliminar_evento)
        btn_delete.grid(row=0, column=0, sticky="ew", pady=(0,6))

        btn_salir = ttk.Button(self.frame_actions, text="Salir", command=self.salir)
        btn_salir.grid(row=1, column=0, sticky="ew")

        # Pequeña instrucción sobre formato de fecha si tkcalendar no está disponible
        if not TKCALENDAR_AVAILABLE:
            info_lbl = ttk.Label(self.frame_entry, text="(Si no tienes tkcalendar instalado usa formato YYYY-MM-DD para la fecha)")
            info_lbl.grid(row=5, column=0, columnspan=2, sticky="w", pady=(6,0))

    def _configure_treeview(self):
        """Opcional: Vinculaciones del Treeview (doble clic para editar/mostrar)."""
        # Doble-click muestra detalles en un popup
        self.tree.bind("<Double-1>", self._on_tree_double_click)

    def _clear_placeholder_fecha(self, event):
        """Limpia el placeholder de la entrada de fecha al hacer foco."""
        if self.entry_fecha.get() == "YYYY-MM-DD":
            self.entry_fecha.delete(0, tk.END)

    def validar_fecha(self, fecha_texto):
        """Valida el formato de fecha 'YYYY-MM-DD'. Devuelve True/False."""
        try:
            datetime.strptime(fecha_texto, "%Y-%m-%d")
            return True
        except Exception:
            return False

    def validar_hora(self, hora_texto):
        """Valida el formato de hora 'HH:MM' (24h)."""
        try:
            datetime.strptime(hora_texto, "%H:%M")
            return True
        except Exception:
            return False

    def agregar_evento(self):
        """Toma los valores de las entradas, valida y agrega un evento al Treeview."""
        fecha = self.entry_fecha.get().strip()
        hora = self.entry_hora.get().strip()
        desc = self.entry_desc.get().strip()

        # Validaciones básicas
        if not fecha:
            messagebox.showwarning("Fecha requerida", "Por favor introduce una fecha para el evento.")
            return

        if TKCALENDAR_AVAILABLE:
            # Si usamos DateEntry ya está en formato correcto, pero validamos por seguridad
            # DateEntry devuelve un objeto tipo datetime.date en algunos casos, así que convertimos a string
            if hasattr(fecha, "strftime"):
                fecha = fecha.strftime("%Y-%m-%d")
        else:
            if not self.validar_fecha(fecha):
                messagebox.showwarning("Formato de fecha inválido", "Introduce la fecha en formato YYYY-MM-DD.")
                return

        if not hora or not self.validar_hora(hora):
            messagebox.showwarning("Hora inválida", "Introduce la hora en formato HH:MM (24 horas).")
            return

        if not desc:
            messagebox.showwarning("Descripción vacía", "Introduce una breve descripción para el evento.")
            return

        # Insertar en Treeview con un ID único
        item_id = f"EV{self._next_id}"
        self.tree.insert("", "end", iid=item_id, values=(fecha, hora, desc))
        self._next_id += 1

        # Limpiar entradas después de añadir
        if not TKCALENDAR_AVAILABLE:
            self.entry_fecha.delete(0, tk.END)
            self.entry_fecha.insert(0, "YYYY-MM-DD")
        else:
            # si se desea, se puede establecer a la fecha actual
            pass
        self.entry_hora.delete(0, tk.END)
        self.entry_hora.insert(0, "09:00")
        self.entry_desc.delete(0, tk.END)

    def eliminar_evento(self):
        """Elimina el evento seleccionado después de confirmación."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Selecciona un evento", "Por favor selecciona un evento para eliminar.")
            return

        # Preguntar confirmación
        respuesta = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que deseas eliminar el evento seleccionado?")
        if not respuesta:
            return

        for item in selected:
            self.tree.delete(item)

    def _on_tree_double_click(self, event):
        """Muestra un popup con los detalles del evento al hacer doble clic."""
        selected = self.tree.selection()
        if not selected:
            return
        item = selected[0]
        vals = self.tree.item(item, "values")
        fecha, hora, desc = vals
        messagebox.showinfo("Detalle del evento", f"Fecha: {fecha}\nHora: {hora}\nDescripción:\n{desc}")

    def salir(self):
        """Cierre seguro de la aplicación (con confirmación opcional)."""
        if messagebox.askokcancel("Salir", "¿Deseas salir de la agenda?"):
            self.destroy()


if __name__ == "__main__":
    # Mensaje informativo sobre tkcalendar
    if not TKCALENDAR_AVAILABLE:
        print("Nota: 'tkcalendar' no está instalado. La aplicación seguirá funcionando,")
        print("pero sin DatePicker. Para instalarlo ejecuta: pip install tkcalendar")
    app = AgendaApp()
    app.mainloop()
