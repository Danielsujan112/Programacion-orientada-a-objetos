import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tareas - Tkinter")
        self.root.geometry("520x380")
        self.root.resizable(False, False)

        # Datos: lista de diccionarios {'text': str, 'done': bool}
        self.tasks = []

        self._setup_ui()
        self._bind_shortcuts()

    def _setup_ui(self):
        pad = 8

        frame_top = tk.Frame(self.root)
        frame_top.pack(fill="x", padx=pad, pady=(pad, 0))

        self.entry = tk.Entry(frame_top, font=(None, 12))
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.focus_set()

        btn_add = tk.Button(frame_top, text="Añadir", width=10, command=self.add_task)
        btn_add.pack(side="left", padx=(6, 0))

        frame_middle = tk.Frame(self.root)
        frame_middle.pack(fill="both", expand=True, padx=pad, pady=(6, 0))

        # Listbox con scrollbar
        self.listbox = tk.Listbox(frame_middle, font=(None, 12), activestyle='none', selectmode=tk.SINGLE)
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_middle, command=self.listbox.yview)
        scrollbar.pack(side="left", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Panel de botones a la derecha
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack(fill="x", padx=pad, pady=(6, pad))

        btn_complete = tk.Button(frame_buttons, text="Marcar completada (C)", command=self.mark_completed)
        btn_complete.pack(side="left")

        btn_delete = tk.Button(frame_buttons, text="Eliminar (Del / D)", command=self.delete_task)
        btn_delete.pack(side="left", padx=6)

        btn_clear_all = tk.Button(frame_buttons, text="Limpiar completadas", command=self.clear_completed)
        btn_clear_all.pack(side="left")

        # Label de estado
        self.status_var = tk.StringVar(value="Listo")
        lbl_status = tk.Label(self.root, textvariable=self.status_var, anchor='w')
        lbl_status.pack(fill="x", padx=pad, pady=(4, pad))

        # Bindings locales
        self.entry.bind("<Return>", lambda e: self.add_task())
        self.listbox.bind('<Double-1>', lambda e: self.toggle_selected_done())

    def _bind_shortcuts(self):
        # Atajos globales
        self.root.bind('<c>', lambda e: self.mark_completed())
        self.root.bind('<C>', lambda e: self.mark_completed())
        self.root.bind('<Delete>', lambda e: self.delete_task())
        self.root.bind('<d>', lambda e: self.delete_task())
        self.root.bind('<D>', lambda e: self.delete_task())
        self.root.bind('<Escape>', lambda e: self.root.destroy())

    # ---------- Operaciones de tareas ----------
    def add_task(self):
        text = self.entry.get().strip()
        if not text:
            self._set_status("No puedes añadir una tarea vacía.")
            return
        self.tasks.append({'text': text, 'done': False})
        self.entry.delete(0, tk.END)
        self._set_status(f"Tarea añadida: {text}")
        self._refresh_listbox()

    def mark_completed(self):
        sel = self.listbox.curselection()
        if not sel:
            self._set_status('Selecciona una tarea para marcarla como completada.')
            return
        idx = sel[0]
        self.tasks[idx]['done'] = True
        self._set_status(f"Tarea marcada como completada: {self.tasks[idx]['text']}")
        self._refresh_listbox()

    def delete_task(self):
        sel = self.listbox.curselection()
        if not sel:
            self._set_status('Selecciona una tarea para eliminarla.')
            return
        idx = sel[0]
        text = self.tasks[idx]['text']
        del self.tasks[idx]
        self._set_status(f"Tarea eliminada: {text}")
        self._refresh_listbox()

    def clear_completed(self):
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if not t['done']]
        removed = before - len(self.tasks)
        self._set_status(f"Se eliminaron {removed} tareas completadas.")
        self._refresh_listbox()

    def toggle_selected_done(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        self.tasks[idx]['done'] = not self.tasks[idx]['done']
        state = 'completada' if self.tasks[idx]['done'] else 'pendiente'
        self._set_status(f"Tarea {state}: {self.tasks[idx]['text']}")
        self._refresh_listbox()

    # ---------- UI helpers ----------
    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for i, t in enumerate(self.tasks):
            display = ("✓ "+t['text']) if t['done'] else t['text']
            self.listbox.insert(tk.END, display)
            # Visual feedback: tareas completadas en gris y cursiva si es posible
            try:
                if t['done']:
                    # itemconfig acepta opciones como fg
                    self.listbox.itemconfig(i, fg='gray')
                else:
                    # restaurar color por defecto
                    self.listbox.itemconfig(i, fg='black')
            except Exception:
                # Si la plataforma/tkinter no soporta itemconfig, no hacemos nada
                pass

    def _set_status(self, text):
        self.status_var.set(text)


if __name__ == '__main__':
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
