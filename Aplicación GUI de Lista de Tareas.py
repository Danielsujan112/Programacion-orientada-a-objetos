""
import tkinter as tk
from tkinter import ttk, font, messagebox

class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lista de Tareas - Tkinter")
        self.geometry("560x380")
        self.minsize(480, 320)
        self.configure(padx=12, pady=12)

        # --- Styling ---
        self.style = ttk.Style(self)
        # Use default theme and tweak fonts/padding for a clean look
        try:
            self.style.theme_use('clam')
        except Exception:
            pass

        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=10)

        # Fonts used for normal and completed tasks (overstrike indicates completed)
        self.font_normal = font.Font(family=default_font.actual('family'), size=10, weight='normal')
        self.font_completed = font.Font(family=default_font.actual('family'), size=10, weight='normal', overstrike=1)

        # --- Data structures ---
        # We'll keep a simple internal dict mapping tree item ID -> completed(bool)
        self._task_state = {}

        # --- UI Layout ---
        self._create_input_area()
        self._create_task_list()
        self._create_buttons()
        self._create_bindings()

    def _create_input_area(self):
        """Create entry + label for adding tasks."""
        frm = ttk.Frame(self)
        frm.pack(fill="x", pady=(0,8))

        lbl = ttk.Label(frm, text="Nueva tarea:")
        lbl.pack(side="left", padx=(0,6))

        self.entry_task = ttk.Entry(frm)
        self.entry_task.pack(side="left", fill="x", expand=True)
        self.entry_task.focus_set()

        # Add via Enter key (bound later) or button
        btn_add = ttk.Button(frm, text="Añadir Tarea", command=self.add_task)
        btn_add.pack(side="left", padx=(8,0))
    
    def _create_task_list(self):
        """Create a Treeview to display tasks with a vertical scrollbar."""
        frm = ttk.Frame(self)
        frm.pack(fill="both", expand=True)

        columns = ("task",)
        self.tree = ttk.Treeview(frm, columns=columns, show="tree")  # using tree column for simpler display
        self.tree.pack(side="left", fill="both", expand=True)

        sb = ttk.Scrollbar(frm, orient="vertical", command=self.tree.yview)
        sb.pack(side="left", fill="y")
        self.tree.configure(yscrollcommand=sb.set)

        # Configure tags for styling
        self.tree.tag_configure("completed", font=self.font_completed, foreground="#6b6b6b")
        self.tree.tag_configure("pending", font=self.font_normal, foreground="#000000")

    def _create_buttons(self):
        """Create action buttons below the task list."""
        frm = ttk.Frame(self)
        frm.pack(fill="x", pady=(8,0))

        btn_complete = ttk.Button(frm, text="Marcar como Completada", command=self.toggle_selected_completed)
        btn_complete.pack(side="left")

        btn_delete = ttk.Button(frm, text="Eliminar Tarea", command=self.delete_selected)
        btn_delete.pack(side="left", padx=(8,0))

        btn_clear_completed = ttk.Button(frm, text="Eliminar completadas", command=self.delete_completed)
        btn_clear_completed.pack(side="right")

    def _create_bindings(self):
        """Bind keys and double-click events."""
        # Enter in entry adds task
        self.entry_task.bind("<Return>", self._on_entry_return)

        # Double-click on item toggles completed state
        self.tree.bind("<Double-1>", self._on_tree_double_click)

        # Delete key removes selected tasks
        self.bind("<Delete>", lambda e: self.delete_selected())

        # Ctrl+Enter also adds a task (anywhere in the window)
        self.bind_all("<Control-Return>", lambda e: self.add_task())

    # ---- Event Handlers / Logic ----
    def _on_entry_return(self, event):
        self.add_task()

    def _on_tree_double_click(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.toggle_completed(item)

    def add_task(self):
        """Add a new task from the entry to the list."""
        text = self.entry_task.get().strip()
        if not text:
            # Nothing to add
            return
        # Insert at the end. Use 'pending' tag by default.
        item_id = self.tree.insert("", "end", text=text, tags=("pending",))
        self._task_state[item_id] = False  # False == not completed
        # Clear entry and keep focus for quick entry
        self.entry_task.delete(0, tk.END)
        self.entry_task.focus_set()

    def get_selected_items(self):
        """Return a tuple of selected item ids (or empty tuple)."""
        return self.tree.selection()

    def toggle_selected_completed(self):
        """Toggle completed state for all selected items (useful for multi-select)."""
        selected = self.get_selected_items()
        if not selected:
            messagebox.showinfo("Info", "Selecciona al menos una tarea para marcar como completada.")
            return
        for item in selected:
            self.toggle_completed(item)

    def toggle_completed(self, item):
        """Toggle completed state for a single tree item (by id)."""
        current = self._task_state.get(item, False)
        new_state = not current
        self._task_state[item] = new_state
        # Update visual tag
        if new_state:
            # mark completed
            self.tree.item(item, tags=("completed",))
        else:
            self.tree.item(item, tags=("pending",))

    def delete_selected(self):
        """Delete selected task(s) from the tree and internal state."""
        selected = self.get_selected_items()
        if not selected:
            messagebox.showinfo("Info", "Selecciona una tarea para eliminar.")
            return
        for item in selected:
            self._task_state.pop(item, None)
            self.tree.delete(item)

    def delete_completed(self):
        """Delete all tasks that are marked completed."""
        items = list(self._task_state.items())
        to_delete = [item for item, done in items if done]
        for item in to_delete:
            self._task_state.pop(item, None)
            try:
                self.tree.delete(item)
            except Exception:
                pass

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
