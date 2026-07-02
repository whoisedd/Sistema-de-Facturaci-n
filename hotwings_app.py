import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font


DATA_FILE = "clientes_hotwings.json"
SALSAS = [
    "Original BBQ",
    "Atomic Suicide",
    "Lemon Pepper",
    "Mango Habanero",
    "Garlic Parmesan",
    "Buffalo Classic",
]
NIVELES_PICANTE = ["Bajo", "Medio", "Alto", "Extremo"]

COLOR_BG = "#1a1a2e"
COLOR_SECONDARY = "#2d2d44"
COLOR_ACCENT = "#e63946"
COLOR_ACCENT_HOVER = "#ff6d00"
COLOR_TEXT = "#ffffff"
COLOR_ENTRY_BG = "#3a3a5c"
COLOR_SELECT = "#e63946"


class HotWingsApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Gesti\u00f3n de Clientes - Hot Wings")
        self.root.configure(bg=COLOR_BG)
        self.root.geometry("1000x620")
        self.root.minsize(900, 560)

        self.clientes: list[dict] = []
        self.selected_id: int | None = None

        self._configure_styles()
        self._build_ui()
        self._cargar_datos()

    # ------------------------------------------------------------------ #
    #  Estilos ttk
    # ------------------------------------------------------------------ #
    def _configure_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure("Treeview",
                        background=COLOR_SECONDARY,
                        foreground=COLOR_TEXT,
                        fieldbackground=COLOR_SECONDARY,
                        rowheight=28,
                        font=("Segoe UI", 10))
        style.map("Treeview",
                  background=[("selected", COLOR_SELECT)],
                  foreground=[("selected", COLOR_TEXT)])

        style.configure("Treeview.Heading",
                        background=COLOR_ACCENT,
                        foreground=COLOR_TEXT,
                        font=("Segoe UI", 10, "bold"),
                        borderwidth=0)
        style.map("Treeview.Heading",
                  background=[("active", COLOR_ACCENT_HOVER)])

        style.configure("TButton",
                        background=COLOR_ACCENT,
                        foreground=COLOR_TEXT,
                        font=("Segoe UI", 10, "bold"),
                        borderwidth=0,
                        padding=(12, 6))
        style.map("TButton",
                  background=[("active", COLOR_ACCENT_HOVER),
                              ("pressed", "#b30000")])

        style.configure("Secondary.TButton",
                        background=COLOR_SECONDARY,
                        foreground=COLOR_TEXT,
                        font=("Segoe UI", 10, "bold"),
                        borderwidth=0,
                        padding=(12, 6))
        style.map("Secondary.TButton",
                  background=[("active", "#4a4a6c"),
                              ("pressed", "#3a3a5c")])

        style.configure("Danger.TButton",
                        background="#8b0000",
                        foreground=COLOR_TEXT,
                        font=("Segoe UI", 10, "bold"),
                        borderwidth=0,
                        padding=(12, 6))
        style.map("Danger.TButton",
                  background=[("active", "#cc0000"),
                              ("pressed", "#660000")])

        style.configure("TLabel",
                        background=COLOR_BG,
                        foreground=COLOR_TEXT,
                        font=("Segoe UI", 10))
        style.configure("Title.TLabel",
                        background=COLOR_BG,
                        foreground=COLOR_ACCENT,
                        font=("Segoe UI", 18, "bold"))
        style.configure("TFrame", background=COLOR_BG)

    # ------------------------------------------------------------------ #
    #  Construcción de la GUI
    # ------------------------------------------------------------------ #
    def _build_ui(self):
        # contenedor principal con padding
        main = ttk.Frame(self.root, padding=16)
        main.pack(fill=tk.BOTH, expand=True)

        # -------------------------------------------------------- #
        #  Panel izquierdo — formulario
        # -------------------------------------------------------- #
        left = ttk.Frame(main, width=340)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 16))
        left.pack_propagate(False)

        # Banner / logo de texto
        banner = ttk.Label(left, text="HOT WINGS", style="Title.TLabel")
        banner.pack(pady=(0, 2))

        subtitle = ttk.Label(left, text="Gesti\u00f3n de Clientes",
                             font=("Segoe UI", 11),
                             foreground="#cccccc", background=COLOR_BG)
        subtitle.pack(pady=(0, 16))

        # Formulario
        form_frame = tk.Frame(left, bg=COLOR_SECONDARY,
                              highlightbackground=COLOR_ACCENT,
                              highlightthickness=1)
        form_frame.pack(fill=tk.X, pady=(0, 14))

        for w in (form_frame,):
            pass  # se usará abajo

        fields = [
            ("ID \u00danico (RUT/DNI)", "entry_id"),
            ("Nombre Completo", "entry_nombre"),
            ("Tel\u00e9fono de Contacto", "entry_telefono"),
            ("\u00daltima Selecci\u00f3n de Salsa", "combo_salsa"),
            ("Nivel de Picante Preferido", "combo_picante"),
        ]

        self._entries: dict[str, tk.Widget] = {}

        for i, (label, key) in enumerate(fields):
            lbl = tk.Label(form_frame, text=label,
                           bg=COLOR_SECONDARY, fg=COLOR_TEXT,
                           font=("Segoe UI", 9), anchor="w")
            lbl.grid(row=i, column=0, sticky="ew", padx=12, pady=(8, 0))

            if key.startswith("combo_"):
                values = SALSAS if "salsa" in key else NIVELES_PICANTE
                combo = ttk.Combobox(form_frame, values=values,
                                     state="readonly",
                                     font=("Segoe UI", 10))
                combo.set("")
                combo.grid(row=i, column=1, padx=12, pady=(4, 8),
                           sticky="ew", ipady=2)
                self._entries[key] = combo
            else:
                entry = tk.Entry(form_frame,
                                 bg=COLOR_ENTRY_BG, fg=COLOR_TEXT,
                                 font=("Segoe UI", 10),
                                 insertbackground=COLOR_TEXT,
                                 relief=tk.FLAT, bd=4)
                entry.grid(row=i, column=1, padx=12, pady=(4, 8),
                           sticky="ew", ipady=2)
                self._entries[key] = entry

            form_frame.columnconfigure(1, weight=1)

        # Botones
        btn_frame = tk.Frame(left, bg=COLOR_BG)
        btn_frame.pack(fill=tk.X)

        row1 = tk.Frame(btn_frame, bg=COLOR_BG)
        row1.pack(fill=tk.X, pady=(0, 6))
        btn_add = ttk.Button(row1, text="A\u00f1adir Cliente",
                             command=self._add_cliente)
        btn_add.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

        btn_update = ttk.Button(row1, text="Actualizar Cliente",
                                command=self._update_cliente)
        btn_update.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(4, 0))

        row2 = tk.Frame(btn_frame, bg=COLOR_BG)
        row2.pack(fill=tk.X)
        btn_delete = ttk.Button(row2, text="Eliminar Cliente",
                                style="Danger.TButton",
                                command=self._delete_cliente)
        btn_delete.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

        btn_clear = ttk.Button(row2, text="Limpiar Formulario",
                               style="Secondary.TButton",
                               command=self._clear_form)
        btn_clear.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(4, 0))

        # -------------------------------------------------------- #
        #  Panel derecho — tabla Treeview
        # -------------------------------------------------------- #
        right = ttk.Frame(main)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Barra de búsqueda (opcional pero útil)
        search_frame = tk.Frame(right, bg=COLOR_BG)
        search_frame.pack(fill=tk.X, pady=(0, 8))

        tk.Label(search_frame, text="Buscar:",
                 bg=COLOR_BG, fg=COLOR_TEXT,
                 font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(0, 8))

        self.entry_buscar = tk.Entry(search_frame,
                                     bg=COLOR_ENTRY_BG, fg=COLOR_TEXT,
                                     font=("Segoe UI", 10),
                                     insertbackground=COLOR_TEXT,
                                     relief=tk.FLAT, bd=4)
        self.entry_buscar.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=2)
        self.entry_buscar.bind("<KeyRelease>", self._filtrar_tabla)

        # Treeview
        tree_frame = tk.Frame(right, bg=COLOR_SECONDARY,
                              highlightbackground=COLOR_ACCENT,
                              highlightthickness=1)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "nombre", "telefono", "salsa", "picante")
        self.tree = ttk.Treeview(tree_frame, columns=columns,
                                 show="headings", selectmode="browse")

        col_labels = {
            "id": "ID",
            "nombre": "Nombre Completo",
            "telefono": "Tel\u00e9fono",
            "salsa": "\u00daltima Salsa",
            "picante": "Nivel Picante",
        }
        col_widths = {"id": 90, "nombre": 190, "telefono": 110,
                      "salsa": 150, "picante": 100}

        for col in columns:
            self.tree.heading(col, text=col_labels[col])
            self.tree.column(col, width=col_widths[col],
                             minwidth=col_widths[col])

        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL,
                            command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL,
                            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
                            xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

    # ------------------------------------------------------------------ #
    #  Persistencia JSON
    # ------------------------------------------------------------------ #
    def _cargar_datos(self):
        if not os.path.exists(DATA_FILE):
            self.clientes = []
            self._guardar_datos()
            return

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.clientes = json.load(f)
        except (json.JSONDecodeError, IOError):
            self.clientes = []
            self._guardar_datos()

        self._refrescar_tabla()

    def _guardar_datos(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.clientes, f, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------ #
    #  CRUD
    # ------------------------------------------------------------------ #
    def _add_cliente(self):
        data = self._get_form_data()
        if data is None:
            return

        # Validar ID único
        for c in self.clientes:
            if c["id"] == data["id"]:
                messagebox.showerror(
                    "Error",
                    f"Ya existe un cliente con el ID {data['id']}.")
                return

        self.clientes.append(data)
        self._guardar_datos()
        self._refrescar_tabla()
        self._clear_form()
        messagebox.showinfo("Éxito", "Cliente añadido con éxito.")

    def _update_cliente(self):
        if self.selected_id is None:
            messagebox.showwarning(
                "Sin selección",
                "Seleccione un cliente de la tabla para actualizar.")
            return

        data = self._get_form_data()
        if data is None:
            return

        # Si el ID cambió, verificar que no choque con otro cliente
        nuevo_id = data["id"]
        for c in self.clientes:
            if c["id"] == nuevo_id and c["id"] != self.selected_id:
                messagebox.showerror(
                    "Error",
                    f"El ID {nuevo_id} ya está en uso por otro cliente.")
                return

        for i, c in enumerate(self.clientes):
            if c["id"] == self.selected_id:
                self.clientes[i] = data
                break

        self._guardar_datos()
        self._refrescar_tabla()
        self._clear_form()
        self.selected_id = None
        messagebox.showinfo("Éxito", "Cliente actualizado con éxito.")

    def _delete_cliente(self):
        if self.selected_id is None:
            messagebox.showwarning(
                "Sin selección",
                "Seleccione un cliente de la tabla para eliminar.")
            return

        confirm = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Está seguro de eliminar al cliente seleccionado?",
            icon=messagebox.WARNING)
        if not confirm:
            return

        self.clientes = [c for c in self.clientes
                         if c["id"] != self.selected_id]
        self._guardar_datos()
        self._refrescar_tabla()
        self._clear_form()
        self.selected_id = None
        messagebox.showinfo("Éxito", "Cliente eliminado con éxito.")

    # ------------------------------------------------------------------ #
    #  Utilidades de formulario / tabla
    # ------------------------------------------------------------------ #
    def _get_form_data(self) -> dict | None:
        campos = {
            "id": self._entries["entry_id"].get().strip(),
            "nombre": self._entries["entry_nombre"].get().strip(),
            "telefono": self._entries["entry_telefono"].get().strip(),
            "salsa": self._entries["combo_salsa"].get().strip(),
            "picante": self._entries["combo_picante"].get().strip(),
        }

        for key, val in campos.items():
            if not val:
                messagebox.showerror(
                    "Error",
                    "Todos los campos son obligatorios.")
                return None

        return campos

    def _clear_form(self):
        for key, widget in self._entries.items():
            if isinstance(widget, ttk.Combobox):
                widget.set("")
            else:
                widget.delete(0, tk.END)
        self.selected_id = None

    def _on_tree_select(self, _event=None):
        sel = self.tree.selection()
        if not sel:
            return

        item = self.tree.item(sel[0])
        valores = item["values"]
        if not valores:
            return

        self.selected_id = valores[0]
        self._entries["entry_id"].delete(0, tk.END)
        self._entries["entry_id"].insert(0, valores[0])

        self._entries["entry_nombre"].delete(0, tk.END)
        self._entries["entry_nombre"].insert(0, valores[1])

        self._entries["entry_telefono"].delete(0, tk.END)
        self._entries["entry_telefono"].insert(0, valores[2])

        self._entries["combo_salsa"].set(valores[3])
        self._entries["combo_picante"].set(valores[4])

    def _refrescar_tabla(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for c in self.clientes:
            self.tree.insert("", tk.END, values=(
                c["id"], c["nombre"], c["telefono"],
                c["salsa"], c["picante"],
            ))

    def _filtrar_tabla(self, _event=None):
        texto = self.entry_buscar.get().strip().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)

        for c in self.clientes:
            if (texto in c["id"].lower()
                    or texto in c["nombre"].lower()
                    or texto in c["telefono"].lower()
                    or texto in c["salsa"].lower()
                    or texto in c["picante"].lower()):
                self.tree.insert("", tk.END, values=(
                    c["id"], c["nombre"], c["telefono"],
                    c["salsa"], c["picante"],
                ))


def main():
    root = tk.Tk()
    app = HotWingsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
