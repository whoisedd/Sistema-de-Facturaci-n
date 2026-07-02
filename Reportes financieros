import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Paleta de colores unificada con el equipo
COLOR_BG = "#1a1a2e"
COLOR_SECONDARY = "#2d2d44"
COLOR_ACCENT = "#e63946"
COLOR_TEXT = "#ffffff"
COLOR_ENTRY_BG = "#3a3a5c"

class ReportesFinancierosApp:
    def __init__(self, root, modulo_facturas=None):
        self.root = root
        self.root.title("Módulo de Reportes Financieros")
        self.root.configure(bg=COLOR_BG)
        self.root.geometry("1000x620")
        self.root.minsize(900, 560)
        
        # Conexión con los datos reales del grupo. Si no hay datos, usa una lista de prueba.
        self.modulo_facturas = modulo_facturas
        self.IVA_PORCENTAJE = 0.15  # Ajustar según tu país
        
        self._build_ui()
        self.actualizar_reportes()

    def _build_ui(self):
        """Construye la interfaz gráfica con el estilo del sistema."""
        # Título Principal
        title_label = tk.Label(
            self.root, text="Panel de Reportes Financieros", 
            font=("Arial", 20, "bold"), bg=COLOR_BG, fg=COLOR_TEXT
        )
        title_label.pack(pady=20)

        # Contenedor de Tarjetas Informativas (Dashboard KPI)
        self.kpi_frame = tk.Frame(self.root, bg=COLOR_BG)
        self.kpi_frame.pack(fill="x", padx=40, pady=10)
        
        # Tarjeta 1: Total Facturado
        self.card_total = self._crear_tarjeta(self.kpi_frame, "TOTAL FACTURADO", "$0.00", "#4ade80")
        self.card_total.grid(row=0, column=0, padx=10, sticky="nsew")
        
        # Tarjeta 2: Impuestos Recaudados
        self.card_iva = self._crear_tarjeta(self.kpi_frame, "IVA RECAUDADO (15%)", "$0.00", "#60a5fa")
        self.card_iva.grid(row=0, column=1, padx=10, sticky="nsew")
        
        # Tarjeta 3: Saldo por Cobrar
        self.card_saldo = self._crear_tarjeta(self.kpi_frame, "CUENTAS POR COBRAR", "$0.00", "#fba51a")
        self.card_saldo.grid(row=0, column=2, padx=10, sticky="nsew")
        
        self.kpi_frame.columnconfigure((0, 1, 2), weight=1)

        # Sección Inferior: Detalles del Historial y Botones
        bottom_frame = tk.Frame(self.root, bg=COLOR_BG)
        bottom_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Estilo para la Tabla (Treeview)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=COLOR_SECONDARY, fieldbackground=COLOR_SECONDARY, foreground=COLOR_TEXT, borderwidth=0, font=("Arial", 11))
        style.configure("Treeview.Heading", background=COLOR_ENTRY_BG, foreground=COLOR_TEXT, font=("Arial", 11, "bold"))
        style.map("Treeview", background=[("selected", COLOR_ACCENT)])

        # Tabla de Comprobantes para auditoría visual
        self.tabla_frame = tk.LabelFrame(bottom_frame, text=" Desglose de Comprobantes Auditados ", bg=COLOR_BG, fg=COLOR_TEXT, font=("Arial", 12, "bold"))
        self.tabla_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        columnas = ("id", "monto", "pagado", "saldo", "estado")
        self.tree = ttk.Treeview(self.tabla_frame, columns=columnas, show="headings")
        self.tree.heading("id", text="ID Factura")
        self.tree.heading("monto", text="Monto Total")
        self.tree.heading("pagado", text="Pagado")
        self.tree.heading("saldo", text="Saldo Pendiente")
        self.tree.heading("estado", text="Estado")
        
        self.tree.column("id", width=120, anchor="center")
        self.tree.column("monto", width=100, anchor="e")
        self.tree.column("pagado", width=100, anchor="e")
        self.tree.column("saldo", width=100, anchor="e")
        self.tree.column("estado", width=100, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Panel de Acciones (Botones)
        btn_frame = tk.Frame(bottom_frame, bg=COLOR_BG)
        btn_frame.pack(side="right", fill="y", padx=(10, 0))

        btn_actualizar = tk.Button(
            btn_frame, text="🔄 Actualizar Datos", font=("Arial", 11, "bold"),
            bg=COLOR_ENTRY_BG, fg=COLOR_TEXT, activebackground=COLOR_ACCENT, 
            activeforeground=COLOR_TEXT, bd=0, width=18, height=2, command=self.actualizar_reportes
        )
        btn_actualizar.pack(pady=10)

        btn_alerta = tk.Button(
            btn_frame, text="⚠️ Alerta de Deudas", font=("Arial", 11, "bold"),
            bg="#b91c1c", fg=COLOR_TEXT, activebackground=COLOR_ACCENT, 
            activeforeground=COLOR_TEXT, bd=0, width=18, height=2, command=self.verificar_deudores
        )
        btn_alerta.pack(pady=10)

    def _crear_tarjeta(self, parent, titulo, valor_inicial, color_valor):
        """Helper para generar tarjetas KPI de aspecto moderno."""
        frame = tk.Frame(parent, bg=COLOR_SECONDARY, bd=1, relief="flat", highlightbackground=COLOR_ENTRY_BG, highlightthickness=1)
        lbl_title = tk.Label(frame, text=titulo, font=("Arial", 10, "bold"), bg=COLOR_SECONDARY, fg="#94a3b8")
        lbl_title.pack(pady=(15, 5), padx=15, anchor="w")
        lbl_val = tk.Label(frame, text=valor_inicial, font=("Arial", 22, "bold"), bg=COLOR_SECONDARY, fg=color_valor)
        lbl_val.pack(pady=(0, 15), padx=15, anchor="w")
        frame.lbl_val = lbl_val  # Guardar referencia para actualizar el texto después
        return frame

    def obtener_facturas(self):
        """Lee las facturas del sistema real o carga unas de prueba estructuradas exactamente igual."""
        if self.modulo_facturas and hasattr(self.modulo_facturas, 'facturas'):
            return self.modulo_facturas.facturas
        
        # Datos simulados idénticos a los del equipo (según la imagen del código de Cuentas por Cobrar)
        return [
            {"id_factura": "FAC-001", "monto_total": 115.00, "pagado": 115.00, "saldo": 0.00, "estado": "PAGADO"},
            {"id_factura": "FAC-002", "monto_total": 230.00, "pagado": 100.00, "saldo": 130.00, "estado": "PENDIENTE"},
            {"id_factura": "FAC-003", "monto_total": 45.00, "pagado": 0.00, "saldo": 45.00, "estado": "PENDIENTE"},
            {"id_factura": "FAC-004", "monto_total": 150.00, "pagado": 150.00, "saldo": 0.00, "estado": "PAGADO"}
        ]

    def actualizar_reportes(self):
        """Efectúa los cálculos matemáticos financieros y refresca la UI."""
        facturas = self.obtener_facturas()
        
        # Limpiar la tabla anterior
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        total_facturado = 0.0
        total_saldo = 0.0
        
        for f in facturas:
            monto = f["monto_total"]
            saldo = f["saldo"]
            pagado = f["pagado"]
            estado = f["estado"]
            
            total_facturado += monto
            total_saldo += saldo
            
            # Insertar en la tabla visual de auditoría
            self.tree.insert("", "end", values=(f["id_factura"], f"${monto:.2f}", f"${pagado:.2f}", f"${saldo:.2f}", estado))
            
        # Calcular el IVA recaudado basado en el total neto facturado
        # Subtotal = Total / (1 + IVA) -> IVA Recaudado = Total - Subtotal
        subtotal = total_facturado / (1 + self.IVA_PORCENTAJE)
        total_iva = total_facturado - subtotal
        
        # Actualizar los textos de los KPIs en la pantalla
        self.card_total.lbl_val.config(text=f"${total_facturado:,.2f}")
        self.card_iva.lbl_val.config(text=f"${total_iva:,.2f}")
        self.card_saldo.lbl_val.config(text=f"${total_saldo:,.2f}")

    def verificar_deudores(self):
        """Revisa si hay cuentas pendientes y emite una alerta gráfica."""
        facturas = self.obtener_facturas()
        pendientes = [f["id_factura"] for f in facturas if f["estado"] == "PENDIENTE"]
        
        if pendientes:
            messagebox.showwarning("Auditoría de Riesgo", f"¡Atención! Existen {len(pendientes)} facturas con saldos PENDIENTES de cobro.")
        else:
            messagebox.showinfo("Auditoría Limpia", "Excelente historial: No se registran saldos pendientes de cobro.")

# Ejecución autónoma para que lo pruebes tú solo
if __name__ == "__main__":
    root = tk.Tk()
    app = ReportesFinancierosApp(root)
    root.mainloop()

    import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# =====================================================================
# CONFIGURACIÓN VISUAL (Mismos colores que usan tus compañeros)
# =====================================================================
COLOR_BG = "#1a1a2e"          # Fondo principal oscuro
COLOR_SECONDARY = "#2d2d44"   # Fondo de tarjetas y tablas
COLOR_ACCENT = "#e63946"      # Color de realce (Rojo/Coral)
COLOR_TEXT = "#ffffff"        # Texto blanco
COLOR_ENTRY_BG = "#3a3a5c"    # Fondo de botones y campos

class ReportesFinancierosApp:
    def __init__(self, root, modulo_facturas=None):
        self.root = root
        self.root.title("Módulo de Reportes Financieros")
        self.root.configure(bg=COLOR_BG)
        self.root.geometry("1000x620")
        self.root.minsize(900, 560)
        
        # Conexión con los datos del grupo (si no hay, usa datos de prueba)
        self.modulo_facturas = modulo_facturas
        self.IVA_PORCENTAJE = 0.15  # 15% de IVA (puedes cambiarlo al 12% si prefieres)
        
        # Construir la interfaz de usuario
        self._build_ui()
        # Calcular y mostrar los datos inmediatamente al abrir
        self.actualizar_reportes()

    def _build_ui(self):
        """Genera todos los componentes visuales de la interfaz."""
        
        # 1. ENCABEZADO
        title_label = tk.Label(
            self.root, text="📊 Panel de Reportes Financieros & Auditoría", 
            font=("Arial", 20, "bold"), bg=COLOR_BG, fg=COLOR_TEXT
        )
        title_label.pack(pady=20)

        # 2. CONTENEDOR DE TARJETAS (Dashboard de control financiero)
        self.kpi_frame = tk.Frame(self.root, bg=COLOR_BG)
        self.kpi_frame.pack(fill="x", padx=40, pady=10)
        
        # Crear Tarjetas KPI individuales
        self.card_total = self._crear_tarjeta(self.kpi_frame, "TOTAL FACTURADO", "$0.00", "#4ade80")
        self.card_total.grid(row=0, column=0, padx=10, sticky="nsew")
        
        self.card_iva = self._crear_tarjeta(self.kpi_frame, f"IVA RECAUDADO ({int(self.IVA_PORCENTAJE*100)}%)", "$0.00", "#60a5fa")
        self.card_iva.grid(row=0, column=1, padx=10, sticky="nsew")
        
        self.card_saldo = self._crear_tarjeta(self.kpi_frame, "CUENTAS POR COBRAR (DEUDAS)", "$0.00", "#fba51a")
        self.card_saldo.grid(row=0, column=2, padx=10, sticky="nsew")
        
        self.kpi_frame.columnconfigure((0, 1, 2), weight=1)

        # 3. SECCIÓN INFERIOR (Tabla de datos y Botones de acción)
        bottom_frame = tk.Frame(self.root, bg=COLOR_BG)
        bottom_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Configurar diseño oscuro para las tablas de Tkinter (Treeview)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=COLOR_SECONDARY, fieldbackground=COLOR_SECONDARY, foreground=COLOR_TEXT, borderwidth=0, font=("Arial", 11))
        style.configure("Treeview.Heading", background=COLOR_ENTRY_BG, foreground=COLOR_TEXT, font=("Arial", 11, "bold"))
        style.map("Treeview", background=[("selected", COLOR_ACCENT)])

        # Tabla contenedora para la auditoría visual
        self.tabla_frame = tk.LabelFrame(bottom_frame, text=" Historial de Comprobantes Auditados ", bg=COLOR_BG, fg=COLOR_TEXT, font=("Arial", 12, "bold"))
        self.tabla_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Columnas basadas en la estructura del archivo 'Cuentas por cobrar.py' de tu equipo
        columnas = ("id", "monto", "pagado", "saldo", "estado")
        self.tree = ttk.Treeview(self.tabla_frame, columns=columnas, show="headings")
        self.tree.heading("id", text="ID Factura")
        self.tree.heading("monto", text="Monto Total")
        self.tree.heading("pagado", text="Monto Pagado")
        self.tree.heading("saldo", text="Saldo Pendiente")
        self.tree.heading("estado", text="Estado")
        
        self.tree.column("id", width=120, anchor="center")
        self.tree.column("monto", width=100, anchor="e")
        self.tree.column("pagado", width=100, anchor="e")
        self.tree.column("saldo", width=100, anchor="e")
        self.tree.column("estado", width=110, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Lateral Derecho: Panel de Botones
        btn_frame = tk.Frame(bottom_frame, bg=COLOR_BG)
        btn_frame.pack(side="right", fill="y", padx=(10, 0))

        # Botón para recalcular valores
        btn_actualizar = tk.Button(
            btn_frame, text="🔄 Recalcular Cierre", font=("Arial", 11, "bold"),
            bg=COLOR_ENTRY_BG, fg=COLOR_TEXT, activebackground=COLOR_ACCENT, 
            activeforeground=COLOR_TEXT, bd=0, width=18, height=2, command=self.actualizar_reportes
        )
        btn_actualizar.pack(pady=10)

        # Botón de seguridad/auditoría rápida para deudores
        btn_alerta = tk.Button(
            btn_frame, text="⚠️ Alerta de Riesgo", font=("Arial", 11, "bold"),
            bg="#b91c1c", fg=COLOR_TEXT, activebackground=COLOR_ACCENT, 
            activeforeground=COLOR_TEXT, bd=0, width=18, height=2, command=self.verificar_deudores
        )
        btn_alerta.pack(pady=10)

    def _crear_tarjeta(self, parent, titulo, valor_inicial, color_valor):
        """Diseña las tarjetas estilizadas del Dashboard."""
        frame = tk.Frame(parent, bg=COLOR_SECONDARY, bd=1, relief="flat", highlightbackground=COLOR_ENTRY_BG, highlightthickness=1)
        lbl_title = tk.Label(frame, text=titulo, font=("Arial", 9, "bold"), bg=COLOR_SECONDARY, fg="#94a3b8")
        lbl_title.pack(pady=(15, 5), padx=15, anchor="w")
        lbl_val = tk.Label(frame, text=valor_inicial, font=("Arial", 22, "bold"), bg=COLOR_SECONDARY, fg=color_valor)
        lbl_val.pack(pady=(0, 15), padx=15, anchor="w")
        frame.lbl_val = lbl_val  
        return frame

    def obtener_facturas_sistema(self):
        """Conecta con el módulo real de tus compañeros o usa datos espejo."""
        if self.modulo_facturas and hasattr(self.modulo_facturas, 'facturas'):
            return self.modulo_facturas.facturas
        
        # Datos temporales idénticos a los campos del código de tu equipo
        return [
            {"id_factura": "FAC-001", "monto_total": 150.00, "pagado": 150.00, "saldo": 0.00, "estado": "PAGADO"},
            {"id_factura": "FAC-002", "monto_total": 320.00, "pagado": 100.00, "saldo": 220.00, "estado": "PENDIENTE"},
            {"id_factura": "FAC-003", "monto_total": 85.00, "pagado": 0.00, "saldo": 85.00, "estado": "PENDIENTE"},
            {"id_factura": "FAC-004", "monto_total": 450.00, "pagado": 450.00, "saldo": 0.00, "estado": "PAGADO"}
        ]

    def actualizar_reportes(self):
        """Lógica matemática: Calcula ingresos, IVA y llena el Treeview."""
        facturas = self.obtener_facturas_sistema()
        
        # Limpiar filas existentes de la interfaz
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        total_facturado = 0.0
        total_saldo = 0.0
        
        # Recorrer datos y sumarlos
        for f in facturas:
            monto = f["monto_total"]
            saldo = f["saldo"]
            pagado = f["pagado"]
            estado = f["estado"]
            
            total_facturado += monto
            total_saldo += saldo
            
            # Insertar visualmente en la tabla
            self.tree.insert("", "end", values=(f["id_factura"], f"${monto:.2f}", f"${pagado:.2f}", f"${saldo:.2f}", estado))
            
        # Desglose matemático exacto del IVA recaudado
        subtotal = total_facturado / (1 + self.IVA_PORCENTAJE)
        total_iva = total_facturado - subtotal
        
        # Pintar los resultados calculados en los componentes gráficos
        self.card_total.lbl_val.config(text=f"${total_facturado:,.2f}")
        self.card_iva.lbl_val.config(text=f"${total_iva:,.2f}")
        self.card_saldo.lbl_val.config(text=f"${total_saldo:,.2f}")

    def verificar_deudores(self):
        """Ventana emergente de auditoría (Alerta de riesgos)."""
        facturas = self.obtener_facturas_sistema()
        pendientes = [f["id_factura"] for f in facturas if f["estado"] == "PENDIENTE"]
        
        if pendientes:
            messagebox.showwarning("Auditoría de Riesgo", f"¡Alerta! Existen {len(pendientes)} comprobantes con montos PENDIENTES de cobro.")
        else:
            messagebox.showinfo("Auditoría Completa", "No se detectaron deudas activas en el sistema.")

# Inicializador autónomo del módulo
if __name__ == "__main__":
    root = tk.Tk()
    app = ReportesFinancierosApp(root)
    root.mainloop()
