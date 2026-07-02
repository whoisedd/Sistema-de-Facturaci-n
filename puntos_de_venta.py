import tkinter as tk
from tkinter import ttk, messagebox

class Producto:
    def __init__(self, codigo, nombre, precio, stock):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

class PuntoDeVenta:
    IVA = 0.15

    def __init__(self):
        self.carrito = []

    def agregar_producto(self, producto, cantidad):
        if cantidad <= 0:
            print("La cantidad debe ser mayor que cero.")
            return False, "La cantidad debe ser mayor que cero."

        if cantidad > producto.stock:
            print("Stock insuficiente.")
            return False, f"Stock insuficiente. Solo quedan {producto.stock}."

        subtotal = producto.precio * cantidad
        self.carrito.append({
            "producto": producto,
            "cantidad": cantidad,
            "subtotal": subtotal
        })

        producto.stock -= cantidad
        print(f"{producto.nombre} agregado correctamente.")
        return True, "Agregado correctamente al pedido."

    def calcular_subtotal(self):
        return sum(item["subtotal"] for item in self.carrito)

    def calcular_iva(self):
        return self.calcular_subtotal() * self.IVA

    def calcular_total(self):
        return self.calcular_subtotal() + self.calcular_iva()

    def mostrar_factura(self):
        print("\n========= TICKET DE PEDIDO =========")
        for item in self.carrito:
            print(f"{item['producto'].nombre}")
            print(f"Cantidad: {item['cantidad']}")
            print(f"Precio Unitario: ${item['producto'].precio:.2f}")
            print(f"Subtotal: ${item['subtotal']:.2f}")
            print("----------------------------")
        print(f"Subtotal: ${self.calcular_subtotal():.2f}")
        print(f"IVA (15%): ${self.calcular_iva():.2f}")
        print(f"TOTAL A PAGAR: ${self.calcular_total():.2f}")
        print("====================================")

class InterfazPOS:
    def __init__(self, root, venta, inventario):
        self.root = root
        self.venta = venta
        self.inventario = inventario

        self.root.title("Punto de Venta - Alitas")
        self.root.geometry("480x650")
        
        self.color_fondo = "#b71c1c"
        self.color_texto = "white"
        self.root.config(padx=20, pady=20, bg=self.color_fondo)

        tk.Label(root, text="🍗 SISTEMA POS: LOCAL DE ALITAS 🍗", font=("Arial", 14, "bold"), bg=self.color_fondo, fg=self.color_texto).pack(pady=10)

        frame_inputs = tk.Frame(root, bg=self.color_fondo)
        frame_inputs.pack(fill="x", pady=10)

        tk.Label(frame_inputs, text="Menú:", font=("Arial", 10, "bold"), bg=self.color_fondo, fg=self.color_texto).grid(row=0, column=0, sticky="w", pady=5)
        self.combo_productos = ttk.Combobox(frame_inputs, state="readonly", width=35)
        self.combo_productos['values'] = [f"{p.nombre} (${p.precio:.2f})" for p in self.inventario]
        self.combo_productos.grid(row=0, column=1, padx=10, pady=5)
        
        if self.inventario:
            self.combo_productos.current(0) 

        tk.Label(frame_inputs, text="Cantidad:", font=("Arial", 10, "bold"), bg=self.color_fondo, fg=self.color_texto).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_cantidad = tk.Entry(frame_inputs, width=10, font=("Arial", 10))
        self.entry_cantidad.insert(0, "1")
        self.entry_cantidad.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        tk.Button(root, text="Agregar al Pedido", bg="#ff5252", fg="white", activebackground="#ff8a80", font=("Arial", 11, "bold"), command=self.agregar).pack(pady=10)

        tk.Label(root, text="Pedido actual:", font=("Arial", 12, "bold"), bg=self.color_fondo, fg=self.color_texto).pack(anchor="w")
        
        self.pantalla = tk.Text(root, height=15, width=55, bg="#ffebee", font=("Consolas", 10), state=tk.DISABLED)
        self.pantalla.pack(pady=5)

        tk.Button(root, text="Cobrar e Imprimir Ticket", bg="#d32f2f", fg="white", activebackground="#f44336", font=("Arial", 13, "bold"), command=self.imprimir).pack(pady=15)

    def agregar(self):
        idx = self.combo_productos.current()
        if idx == -1: return
        producto = self.inventario[idx]
        
        try:
            cantidad = int(self.entry_cantidad.get())
        except ValueError:
            messagebox.showerror("Error", "Cantidad inválida. Ingresa un número.")
            return

        exito, msj = self.venta.agregar_producto(producto, cantidad)
        if exito:
            self.actualizar_pantalla()
            self.entry_cantidad.delete(0, tk.END)
            self.entry_cantidad.insert(0, "1")
        else:
            messagebox.showwarning("Aviso de Inventario", msj)

    def actualizar_pantalla(self):
        texto = ""
        for item in self.venta.carrito:
            texto += f"🍗 {item['producto'].nombre} (x{item['cantidad']}) \n   -> Subtotal: ${item['subtotal']:.2f}\n"
        
        if self.venta.carrito:
            texto += "----------------------------------------\n"
            texto += f"Subtotal: ${self.venta.calcular_subtotal():.2f}\n"
            texto += f"IVA: ${self.venta.calcular_iva():.2f}\n"
            texto += f"TOTAL: ${self.venta.calcular_total():.2f}"

        self.pantalla.config(state=tk.NORMAL)
        self.pantalla.delete("1.0", tk.END)
        self.pantalla.insert(tk.END, texto)
        self.pantalla.config(state=tk.DISABLED)

    def imprimir(self):
        if not self.venta.carrito:
            messagebox.showinfo("Aviso", "El pedido está vacío.")
            return
        
        self.venta.mostrar_factura()
        messagebox.showinfo("¡Venta Exitosa!", "El pedido ha sido cobrado. El ticket se imprimió en la terminal.")
        
        self.venta.carrito = []
        self.actualizar_pantalla()

if __name__ == "__main__":
    p1 = Producto("AL-01", "Combo Alitas BBQ (6 uds)", 6.50, 30)
    p2 = Producto("AL-02", "Combo Alitas Búfalo Picante (12 uds)", 11.00, 20)
    p3 = Producto("AL-03", "Combo Alitas Maracuyá (8 uds)", 8.00, 25)
    p4 = Producto("EX-01", "Porción Extra de Papas Fritas", 2.50, 50)
    p5 = Producto("BE-01", "Gaseosa Cola 1L", 1.50, 40)
    p6 = Producto("BE-02", "Cerveza Artesanal", 3.00, 30)
    
    inventario_base = [p1, p2, p3, p4, p5, p6]
    venta_actual = PuntoDeVenta()

    root = tk.Tk()
    app = InterfazPOS(root, venta_actual, inventario_base)
    root.mainloop()
