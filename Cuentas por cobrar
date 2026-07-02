import json
import os
import tkinter as tk
from datetime import datetime

DB_CXC = "cuentasxcobrar.json"


class CuentaPorCobrar:
    def __init__(self, cliente):
        self.cliente = cliente
        self.facturas = []

    def agregar_deuda(self, id_factura, monto_total):
        self.facturas.append({
            "id_factura": id_factura,
            "monto_total": float(monto_total),
            "pagado": 0,
            "saldo": float(monto_total),
            "estado": "PENDIENTE",
            "fecha": datetime.now().isoformat()
        })
        return "Deuda registrada"

    def abonar(self, id_factura, monto):
        monto = float(monto)
        for f in self.facturas:
            if f["id_factura"] == id_factura:
                if f["estado"] == "PAGADA":
                    return "La factura ya esta pagada"
                f["pagado"] += monto
                f["saldo"] -= monto
                if f["saldo"] <= 0:
                    f["saldo"] = 0
                    f["estado"] = "PAGADA"
                return "Abono registrado correctamente"
        return "Factura no encontrada"

    def resumen(self):
        texto = f"CLIENTE: {self.cliente}\n\n"
        for f in self.facturas:
            texto += (
                f"Factura: {f['id_factura']}\n"
                f"Total: {f['monto_total']}\n"
                f"Pagado: {f['pagado']}\n"
                f"Saldo: {f['saldo']}\n"
                f"Estado: {f['estado']}\n"
                "-----------------------------\n"
            )
        return texto


def _cargar_cxc():
    if os.path.exists(DB_CXC):
        try:
            with open(DB_CXC, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def _guardar_cxc(data):
    with open(DB_CXC, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def obtener_cuentas():
    return _cargar_cxc()

def agregar_deuda_cxc(id_factura, monto_total):
    data = _cargar_cxc()
    data.append({
        "id_factura": id_factura,
        "monto_total": float(monto_total),
        "pagado": 0,
        "saldo": float(monto_total),
        "estado": "PENDIENTE",
        "fecha": datetime.now().isoformat()
    })
    _guardar_cxc(data)
    return True, "Deuda registrada"

def abonar_cxc(id_factura, monto):
    data = _cargar_cxc()
    for f in data:
        if f["id_factura"] == id_factura:
            if f["estado"] == "PAGADA":
                return False, "La factura ya esta pagada"
            f["pagado"] += float(monto)
            f["saldo"] -= float(monto)
            if f["saldo"] <= 0:
                f["saldo"] = 0
                f["estado"] = "PAGADA"
            _guardar_cxc(data)
            return True, "Abono registrado correctamente"
    return False, "Factura no encontrada"


def main_tkinter():
    cxc = CuentaPorCobrar("Cliente General")
    root = tk.Tk()
    root.title("Cuentas por Cobrar")
    root.geometry("650x550")
    root.config(bg="#8B0000")
    title = tk.Label(root, text="HOT WINGS - CUENTAS POR COBRAR",
                     font=("Arial Black", 16, "bold"), fg="white", bg="#8B0000")
    title.pack(pady=10)
    frame = tk.Frame(root, bg="#B22222", bd=5, relief="ridge")
    frame.pack(pady=10, padx=10, fill="x")
    tk.Label(frame, text="ID FACTURA", bg="#B22222", fg="white").grid(row=0, column=0)
    entry_factura = tk.Entry(frame, width=20)
    entry_factura.grid(row=0, column=1, padx=5, pady=5)
    tk.Label(frame, text="MONTO DEUDA", bg="#B22222", fg="white").grid(row=1, column=0)
    entry_monto = tk.Entry(frame, width=20)
    entry_monto.grid(row=1, column=1, padx=5, pady=5)
    tk.Label(frame, text="ABONO", bg="#B22222", fg="white").grid(row=2, column=0)
    entry_abono = tk.Entry(frame, width=20)
    entry_abono.grid(row=2, column=1, padx=5, pady=5)
    def tk_agregar():
        if entry_factura.get() == "" or entry_monto.get() == "":
            text.insert(tk.END, "\nCampos vacios\n")
            return
        cxc.agregar_deuda(entry_factura.get(), entry_monto.get())
        text.delete("1.0", tk.END)
        text.insert(tk.END, cxc.resumen())
        text.insert(tk.END, "\nDeuda registrada\n")
    def tk_abonar():
        if entry_factura.get() == "" or entry_abono.get() == "":
            text.insert(tk.END, "\nCampos vacios\n")
            return
        msg = cxc.abonar(entry_factura.get(), entry_abono.get())
        text.delete("1.0", tk.END)
        text.insert(tk.END, cxc.resumen())
        text.insert(tk.END, f"\n{msg}\n")
    tk.Button(frame, text="REGISTRAR DEUDA", bg="#FF2400", fg="white",
              command=tk_agregar).grid(row=0, column=2, padx=10)
    tk.Button(frame, text="ABONAR", bg="#CC0000", fg="white",
              command=tk_abonar).grid(row=1, column=2, padx=10)
    text = tk.Text(root, bg="black", fg="lime", font=("Courier", 10), height=18)
    text.pack(padx=10, pady=10, fill="both", expand=True)
    text.insert(tk.END, cxc.resumen())
    root.mainloop()


if __name__ == "__main__":
    main_tkinter()
