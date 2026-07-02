import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import datetime
import re

# --- CONFIGURACIÓN DE PARADIGMA ---
CONFIG_FILE = "banco_config.json"
DATA_CUENTAS_FILE = "banco_cuentas_v4.json"

# --- PALETA NEUROATRACTIVA (ESTILO MATRIX / RUBEDO DE ALTA FRECUENCIA) ---
COLOR_BG = "#030307"          # Vacío cósmico/Abismo de posibilidades
COLOR_CARD = "#090918"        # Contenedor de energía (Templos)
COLOR_TEXT = "#00FF66"        # Verde fósforo (Vitalidad/Acción)
COLOR_TEXT_MUTED = "#88aa99"  # Verde apagado para datos secundarios

# Colores Elementales Estrictos
COLOR_AGUA = "#00FFFF"        # Cian eléctrico (Liquidez/Flujo)
COLOR_BOSQUE = "#33FF33"      # Verde Rubedo (Crecimiento/Acciones)
COLOR_AIRE = "#BB55FF"        # Violeta neón (Futuro/Energías limpias)
COLOR_NUCLEO = "#FF8800"      # Oro/Petróleo (Fuerza de Reserva Central)
COLOR_ETER = "#FF0077"        # Magenta cuántico (Tecnósfera/IA/Red de Silicio)

FONT_HEROICA = ("Courier New", 11, "bold")
FONT_MONITOR = ("Courier New", 20, "bold")

class BancoTaguaTaguaV4_Base:
    """Gestiona el motor de datos local y la persistencia del Ecosistema Financiero."""
    def __init__(self):
        self.cuentas = {}
        self.historial_tasas = [{"fecha": "2026-01-01 00:00", "tasa": 30.0}]
        self.tasa_actual = 30.0
        self.cargar_datos()

    def cargar_datos(self):
        if os.path.exists(DATA_CUENTAS_FILE):
            try:
                with open(DATA_CUENTAS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.cuentas = data.get("cuentas", {})
                    self.historial_tasas = data.get("historial_tasas", [{"fecha": "2026-01-01 00:00", "tasa": 30.0}])
                    self.tasa_actual = self.historial_tasas[-1]["tasa"]
            except Exception:
                self.cuentas = {}
        else:
            self.cuentas = {}

    def guardar_datos(self):
        data = {
            "cuentas": self.cuentas,
            "historial_tasas": self.historial_tasas
        }
        with open(DATA_CUENTAS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def asegurar_cuenta(self, usuario):
        if usuario not in self.cuentas:
            self.cuentas[usuario] = {
                "balance_mu": 0.0,
                "biomasa": {
                    "AGUA_LIQUIDEZ": 100.0,       # Capital inicial de flujo
                    "BOSQUE_CRECIMIENTO": 0.0,    # Acciones
                    "AIRE_FUTURO": 0.0,          # Renovables
                    "NUCLEO_RESERVA": 0.0,        # Oro
                    "ETER_TECNOSFERA": 0.0        # Redes / Big Tech
                },
                "historial_transacciones": []
            }
            self.guardar_datos()

    def registrar_conversion(self, usuario, pv_gastados, mu_obtenidas, tasa_usada):
        self.asegurar_cuenta(usuario)
        self.cuentas[usuario]["balance_mu"] += mu_obtenidas
        # Inyectar directamente a la Liquidez del Agua del usuario
        self.cuentas[usuario]["biomasa"]["AGUA_LIQUIDEZ"] += mu_obtenidas
        
        tx = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tipo": "CONVERSION_PV",
            "pv": pv_gastados,
            "mu": mu_obtenidas,
            "tasa": tasa_usada,
            "detalle": f"Transmutación de {pv_gastados} PV de voluntad"
        }
        self.cuentas[usuario]["historial_transacciones"].append(tx)
        self.guardar_datos()


class AppBancoTaguaTaguaV4(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BANCO TAGUA TAGUA v4.0 — LA BIÓSFERA DEL CAPITAL")
        self.geometry("950x650")
        self.configure(bg=COLOR_BG)
        
        self.engine = BancoTaguaTaguaV4_Base()
        self.usuario_seleccionado = tk.StringVar(value="Selecciona Guerrero")
        
        self._construir_interfaz_neuroatractiva()
        self._actualizar_selector_usuarios()

    def _construir_interfaz_neuroatractiva(self):
        # --- ESTILOS GENERALES TTK ---
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=COLOR_BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=COLOR_CARD, foreground=COLOR_AIRE, font=FONT_HEROICA, padding=6)
        style.map("TNotebook.Tab", background=[("selected", COLOR_BG)], foreground=[("selected", COLOR_TEXT)])

        # ==================== TIMELINE / TOP CONTROL BAR ====================
        top_bar = tk.Frame(self, bg=COLOR_CARD, bd=1, relief="flat", highlightbackground="#111133", highlightthickness=1)
        top_bar.pack(fill="x", padx=15, pady=10)

        # Selector de Guerreros Activos (Cuentas)
        tk.Label(top_bar, text="👤 CUENTA ACTIVA:", font=FONT_HEROICA, bg=COLOR_CARD, fg=COLOR_TEXT).pack(side="left", padx=10, pady=8)
        self.combo_usuarios = ttk.Combobox(top_bar, textvariable=self.usuario_seleccionado, font=FONT_HEROICA, state="readonly")
        self.combo_usuarios.pack(side="left", padx=5)
        self.combo_usuarios.bind("<<ComboboxSelected>>", self._cambiar_usuario)

        tk.Button(top_bar, text="⚡ Despertar Nodo (Nueva Cuenta)", font=("Courier New", 8, "bold"), bg=COLOR_BG, fg=COLOR_AGUA, command=self._crear_cuenta).pack(side="left", padx=10)

        # Control Decretor de Tasa Dinámica
        tasa_frame = tk.Frame(top_bar, bg=COLOR_CARD)
        tasa_frame.pack(side="right", padx=15)
        tk.Label(tasa_frame, text="Decretar Tasa PV->1μ:", font=("Courier New", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(side="left")
        self.ent_tasa = tk.Entry(tasa_frame, width=5, bg=COLOR_BG, fg=COLOR_AGUA, font=FONT_HEROICA, insertbackground=COLOR_AGUA)
        self.ent_tasa.insert(0, str(self.engine.tasa_actual))
        self.ent_tasa.pack(side="left", padx=5)
        tk.Button(tasa_frame, text="Fijar Rumbo", font=("Courier New", 8, "bold"), bg=COLOR_BG, fg=COLOR_TEXT, command=self._decretar_tasa).pack(side="left")

        # ==================== BIOSPHERE REALTIME MONITOR ====================
        self.monitor_frame = tk.Frame(self, bg=COLOR_CARD, bd=1, highlightbackground=COLOR_TEXT, highlightthickness=1)
        self.monitor_frame.pack(fill="x", padx=15, pady=5)
        
        tk.Label(self.monitor_frame, text="✦ MONITOREO DE BIOMASA METABÓLICA ✦", font=FONT_HEROICA, bg=COLOR_CARD, fg=COLOR_AIRE).pack(pady=4)
        
        self.grid_elementos = tk.Frame(self.monitor_frame, bg=COLOR_CARD)
        self.grid_elementos.pack(fill="x", padx=10, pady=5)
        self.grid_elementos.columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.labels_valores = {}
        elementos_config = [
            ("💧 AGUA\n(Liquidez)", "AGUA_LIQUIDEZ", COLOR_AGUA),
            ("🌲 BOSQUE\n(Acciones)", "BOSQUE_CRECIMIENTO", COLOR_BOSQUE),
            ("🔮 AIRE\n(Futuros)", "AIRE_FUTURO", COLOR_AIRE),
            ("🔥 NÚCLEO\n(Reserva)", "NUCLEO_RESERVA", COLOR_NUCLEO),
            ("⚡ ÉTER\n(Tecnósfera)", "ETER_TECNOSFERA", COLOR_ETER)
        ]

        for idx, (nombre, key, color) in enumerate(elementos_config):
            f = tk.Frame(self.grid_elementos, bg=COLOR_BG, bd=1, highlightbackground=color, highlightthickness=1)
            f.grid(row=0, column=idx, padx=4, pady=5, sticky="ew")
            tk.Label(f, text=nombre, font=("Courier New", 9, "bold"), bg=COLOR_BG, fg=color).pack(pady=2)
            lbl_v = tk.Label(f, text="0.00", font=FONT_MONITOR, bg=COLOR_BG, fg="#ffffff")
            lbl_v.pack(pady=4)
            self.labels_valores[key] = lbl_v

        # Totalizador de Energía Cósmica
        self.lbl_total_mu = tk.Label(self.monitor_frame, text="TOTAL MONEDAS CÓSMICAS (μ): 0.00", font=FONT_HEROICA, bg=COLOR_CARD, fg=COLOR_TEXT)
        self.lbl_total_mu.pack(pady=6)

        # ==================== NOTEBOOK DE OPERACIONES ====================
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=10)

        # Capa de Transmutación Básica (PV -> Mu)
        self.tab_transmutar = tk.Frame(self.notebook, bg=COLOR_BG)
        self.notebook.add(self.tab_transmutar, text="⚔ TRANSMUTACIÓN VOLUNTAD")
        self._setup_tab_transmutar()

        # Capa de Alquimia de Mercado (Próxima Capa)
        self.tab_alquimia = tk.Frame(self.notebook, bg=COLOR_BG)
        self.notebook.add(self.tab_alquimia, text="🧬 ALQUIMIA FINANCIERA")
        tk.Label(self.tab_alquimia, text="[Capa 2: Motor de Semillas y Gráficos XY Históricos se acoplará aquí]", font=FONT_HEROICA, bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(expand=True)

    def _setup_tab_transmutar(self):
        content = tk.Frame(self.tab_transmutar, bg=COLOR_CARD, highlightbackground="#111133", highlightthickness=1)
        content.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(content, text="ABSORBER PUNTOS DE VOLUNTAD DESDE EL HUEVO CÓSMICO", font=FONT_HEROICA, bg=COLOR_CARD, fg=COLOR_AGUA).pack(pady=15)
        
        form_frame = tk.Frame(content, bg=COLOR_CARD)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Cantidad de PV a sacrificar:", font=FONT_HEROICA, bg=COLOR_CARD, fg="#ffffff").grid(row=0, column=0, padx=10, pady=5)
        self.ent_pv = tk.Entry(form_frame, bg=COLOR_BG, fg=COLOR_TEXT, font=FONT_HEROICA, insertbackground=COLOR_TEXT, width=10)
        self.ent_pv.grid(row=0, column=1, padx=10, pady=5)

        tk.Button(content, text="💥 CRISTALIZAR EN ENERGÍA METABÓLICA (μ)", font=FONT_HEROICA, bg=COLOR_BG, fg=COLOR_TEXT, bd=2, relief="groove", padding=10, command=self._ejecutar_transmutacion).pack(pady=20)

    def _actualizar_selector_usuarios(self):
        lista = list(self.engine.cuentas.keys())
        if not lista:
            self.combo_usuarios["values"] = ["Sin Nodos"]
            self.usuario_seleccionado.set("Sin Nodos")
        else:
            self.combo_usuarios["values"] = lista
            if self.usuario_seleccionado.get() not in lista:
                self.usuario_seleccionado.set(lista[0])
            self._actualizar_biomasa_visual()

    def _cambiar_usuario(self, event=None):
        self._actualizar_biomasa_visual()

    def _crear_cuenta(self):
        nombre = simpledialog.askstring("Nuevo Nodo", "Ingresa el nombre del Guerrero/Cuenta:", parent=self)
        if nombre:
            nombre_clean = nombre.strip()
            if nombre_clean:
                self.engine.asegurar_cuenta(nombre_clean)
                self.usuario_seleccionado.set(nombre_clean)
                self._actualizar_selector_usuarios()

    def _decretar_tasa(self):
        try:
            nueva_tasa = float(self.ent_tasa.get())
            if nueva_tasa <= 0: raise ValueError
            self.engine.tasa_actual = nueva_tasa
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            self.engine.historial_tasas.append({"fecha": timestamp, "tasa": nueva_tasa})
            self.engine.guardar_datos()
            messagebox.showinfo("Rumbo Fijado", f"Decreto Cósmico: La tasa actual es {nueva_tasa} PV = 1μ")
        except ValueError:
            messagebox.showerror("Error", "La tasa debe ser un número entero o decimal positivo.")

    def _ejecutar_transmutacion(self):
        usuario = self.usuario_seleccionado.get()
        if usuario == "Sin Nodos":
            messagebox.showerror("Error", "Debes crear o despertar un Nodo de cuenta primero.")
            return

        try:
            pv = float(self.ent_pv.get())
            if pv <= 0: raise ValueError
            
            # Algoritmo de conversión dinámico usando tu tasa decretada
            mu_calculadas = pv / self.engine.tasa_actual
            
            self.engine.registrar_conversion(usuario, pv, mu_calculadas, self.engine.tasa_actual)
            self._actualizar_biomasa_visual()
            self.ent_pv.delete(0, tk.END)
            
            messagebox.showinfo("Alquimia Exitosa", f"Has transmutado {pv} PV en +{mu_calculadas:.2f}μ.\n¡La energía fluye hacia el Caudal de Agua!")
        except ValueError:
            messagebox.showerror("Error", "Introduce una cantidad de PV válida (numérica y mayor a cero).")

    def _actualizar_biomasa_visual(self):
        usuario = self.usuario_seleccionado.get()
        if usuario == "Sin Nodos" or usuario not in self.engine.cuentas:
            for k in self.labels_valores:
                self.labels_valores[k].config(text="0.00")
            self.lbl_total_mu.config(text="TOTAL MONEDAS CÓSMICAS (μ): 0.00")
            return

        cuenta = self.engine.cuentas[usuario]
        biomasa = cuenta["biomasa"]
        
        # Actualizar cada elemento orgánico en pantalla
        for key, lbl in self.labels_valores.items():
            lbl.config(text=f"{biomasa.get(key, 0.0):,.2f}")
        
        self.lbl_total_mu.config(text=f"TOTAL MONEDAS CÓSMICAS (μ): {cuenta['balance_mu']:,.2f}")


if __name__ == "__main__":
    app = AppBancoTaguaTaguaV4()
    app.mainloop()
