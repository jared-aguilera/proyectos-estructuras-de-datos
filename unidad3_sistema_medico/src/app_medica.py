import os
import customtkinter as ctk
from tkinter import messagebox
import time
from gestion_datos import GestionHospital

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class AppMedica(ctk.CTk):
    """
    Clase principal que gestiona la interfaz gráfica del sistema médico.
    Permite el registro inmediato, agendamiento de reservas, atención de pacientes,
    visualización de salas de espera, consulta de historial y reportes de eficiencia.
    """

    def __init__(self):
        super().__init__()

        # Inicializar lógica del hospital
        self.hospital = GestionHospital()

        # Configuración de la ventana
        self.title("Sistema de Gestión de Atención Médica")
        self.geometry("1200x750")

        # Nombres legibles para la interfaz
        self.DEPTOS_DISPLAY = {
            "urgencias": "Urgencias",
            "pediatria": "Pediatria",
            "medicina_general": "Medicina General"
        }

        # Grid principal: Fila 0 para Título, Fila 1 para Contenido
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.crear_header()
        
        # Frame contenedor de los 3 paneles principales
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.main_container.grid_columnconfigure((0, 1, 2), weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        self.crear_panel_estadisticas()
        self.crear_panel_registro()
        self.crear_panel_visualizacion()
        
        self.actualizar_estadisticas()
        self.actualizar_tablas()
        
        # Iniciar el verificador automático de reservas (revisa cada 10 segundos)
        self.verificador_automatico()

    def crear_header(self):
        """Genera el título principal centrado en la parte superior."""
        self.header = ctk.CTkLabel(
            self, 
            text="Hospital", 
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.header.grid(row=0, column=0, pady=30)

    def crear_panel_estadisticas(self):
        """Genera el panel izquierdo dedicado a métricas, reportes e histórico."""
        self.panel_stats = ctk.CTkFrame(self.main_container, corner_radius=15, border_width=2)
        self.panel_stats.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(
            self.panel_stats, 
            text="Estadisticas", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)

        # Contenedor para valores
        self.lbl_atendidos = ctk.CTkLabel(self.panel_stats, text="Atendidos: 0", font=ctk.CTkFont(size=14))
        self.lbl_atendidos.pack(pady=10)

        self.lbl_espera = ctk.CTkLabel(self.panel_stats, text="Espera Promedio: 0.0s", font=ctk.CTkFont(size=14))
        self.lbl_espera.pack(pady=10)

        # Botones de reporte y seguimiento histórico
        self.btn_reporte = ctk.CTkButton(
            self.panel_stats, 
            text="Generar Reporte", 
            command=self.mostrar_reporte
        )
        self.btn_reporte.pack(side="bottom", pady=(10, 30))

        self.btn_historico = ctk.CTkButton(
            self.panel_stats,
            text="Ver Historico",
            fg_color="#34495e",
            hover_color="#2c3e50",
            command=self.mostrar_historico
        )
        self.btn_historico.pack(side="bottom", pady=10)

    def crear_panel_registro(self):
        """Genera el panel central con el formulario de registro y agendamiento."""
        self.panel_reg = ctk.CTkFrame(self.main_container, corner_radius=15, border_width=2)
        self.panel_reg.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            self.panel_reg, 
            text="Gestión de Ingreso", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)

        ctk.CTkLabel(self.panel_reg, text="Nombre del Paciente:").pack(pady=(10, 5))
        self.entry_nombre = ctk.CTkEntry(self.panel_reg, placeholder_text="Nombre:", width=250)
        self.entry_nombre.pack(pady=5)

        ctk.CTkLabel(self.panel_reg, text="Departamento:").pack(pady=(10, 5))
        self.menu_depto = ctk.CTkOptionMenu(
            self.panel_reg, 
            values=list(self.DEPTOS_DISPLAY.values()),
            width=200
        )
        self.menu_depto.set("Urgencias")
        self.menu_depto.pack(pady=5)

        # SECCIÓN DE RESERVA CON SELeCTORES
        ctk.CTkLabel(self.panel_reg, text="Hora de Reserva (Opcional):").pack(pady=(15, 0))
        
        self.frame_hora = ctk.CTkFrame(self.panel_reg, fg_color="transparent")
        self.frame_hora.pack(pady=5)
        
        # Generar listas de horas (00-23) y minutos (00-55 de 5 en 5)
        horas = [f"{i:02d}" for i in range(24)]
        minutos = [f"{i:02d}" for i in range(0, 60, 5)]
        
        self.combo_hora = ctk.CTkOptionMenu(self.frame_hora, values=horas, width=70)
        self.combo_hora.set(time.strftime('%H')) # Hora actual por defecto
        self.combo_hora.pack(side="left", padx=2)
        
        ctk.CTkLabel(self.frame_hora, text=":").pack(side="left")
        
        self.combo_min = ctk.CTkOptionMenu(self.frame_hora, values=minutos, width=70)
        self.combo_min.set("00")
        self.combo_min.pack(side="left", padx=2)

        # SECCIÓN DE PRIORIDAD
        ctk.CTkLabel(self.panel_reg, text="Prioridad (Ingreso Inmediato):").pack(pady=(15, 5))
        self.prioridad_var = ctk.IntVar(value=2)
        self.seg_prioridad = ctk.CTkSegmentedButton(
            self.panel_reg, 
            values=["Emergencia", "Regular"],
            command=self.cambiar_prioridad_interna
        )
        self.seg_prioridad.set("Regular")
        self.seg_prioridad.pack(pady=5)

        self.btn_registrar = ctk.CTkButton(
            self.panel_reg, 
            text="Ingreso Inmediato", 
            fg_color="#27ae60", 
            hover_color="#1e8449",
            command=self.registrar
        )
        self.btn_registrar.pack(pady=(30, 10))

        self.btn_reservar = ctk.CTkButton(
            self.panel_reg, 
            text="Agendar Reserva", 
            fg_color="#2980b9", 
            hover_color="#1f618d",
            command=self.reservar
        )
        self.btn_reservar.pack(pady=10)

    def crear_panel_visualizacion(self):
        """Genera el panel derecho con la lista dinámica de la sala de espera."""
        self.panel_view = ctk.CTkFrame(self.main_container, corner_radius=15, border_width=2)
        self.panel_view.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            self.panel_view, 
            text="Sala de Espera", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)

        self.scroll_sala = ctk.CTkScrollableFrame(self.panel_view, width=320, height=350, fg_color="transparent")
        self.scroll_sala.pack(pady=10, padx=15, fill="both", expand=True)

        self.btn_atender = ctk.CTkButton(
            self.panel_view, 
            text="Atender Siguiente", 
            width=200,
            command=self.atender
        )
        self.btn_atender.pack(pady=20)

    # --- LÓGICA DE CONTROL ---

    def verificador_automatico(self):
        """Revisa periódicamente si alguna reserva debe activarse."""
        activados = self.hospital.verificar_reservas()
        if activados:
            self.actualizar_tablas()
            nombres = ", ".join(activados)
            messagebox.showinfo("Cita Activada", f"La hora ha llegado. El paciente {nombres} ha entrado a la sala de espera.")
        
        # Ejecutar de nuevo en 10 segundos
        self.after(10000, self.verificador_automatico)

    def cambiar_prioridad_interna(self, valor):
        """Asigna el valor numérico de prioridad según la selección del botón."""
        self.prioridad_var.set(1 if valor == "Emergencia" else 2)

    def obtener_key_depto(self, display_name):
        """Traduce el nombre visual del departamento a su clave interna."""
        for key, value in self.DEPTOS_DISPLAY.items():
            if value == display_name:
                return key
        return "urgencias"

    def registrar(self):
        """Valida y registra un paciente para ingreso inmediato."""
        nombre = self.entry_nombre.get().strip()
        depto_key = self.obtener_key_depto(self.menu_depto.get())

        exito, mensaje = self.hospital.registrar_paciente(
            nombre, 
            self.prioridad_var.get(), 
            depto_key
        )
        
        if exito:
            self.entry_nombre.delete(0, 'end')
            self.actualizar_tablas()
            messagebox.showinfo("Sistema", mensaje)
        else:
            messagebox.showerror("Validacion", mensaje)

    def reservar(self):
        """Construye la hora desde los selectores y agenda la cita."""
        nombre = self.entry_nombre.get().strip()
        # Construimos el formato HH:MM desde los dropdowns
        hora_citada = f"{self.combo_hora.get()}:{self.combo_min.get()}"
        depto_key = self.obtener_key_depto(self.menu_depto.get())
        
        # El hospital validará si la hora es futura
        exito, mensaje = self.hospital.registrar_reserva(nombre, depto_key, hora_citada)
        if exito:
            self.entry_nombre.delete(0, 'end')
            messagebox.showinfo("Reserva", mensaje)
        else:
            # Aquí saltará el error si el usuario eligió una hora del pasado
            messagebox.showerror("Error de Reserva", mensaje)

    def atender(self):
        """Procesa la atención del siguiente paciente y notifica el turno."""
        depto_key = self.obtener_key_depto(self.menu_depto.get())
        paciente = self.hospital.atender_paciente(depto_key)
        
        if paciente:
            # Notificación visual para el paciente
            messagebox.showinfo(
                "Notificación", 
                f"Paciente {paciente.nombre} favor de pasar a {self.DEPTOS_DISPLAY[depto_key]}."
            )
            self.actualizar_tablas()
            self.actualizar_estadisticas()
        else:
            messagebox.showwarning("Sala Vacia", "No hay pacientes en este departamento.")

    def actualizar_tablas(self):
        """Actualiza visualmente la sala de espera centrando títulos y estados."""
        for widget in self.scroll_sala.winfo_children():
            widget.destroy()
        
        for depto_key, cola in self.hospital.departamentos.items():
            lbl_depto = ctk.CTkLabel(
                self.scroll_sala, 
                text=self.DEPTOS_DISPLAY[depto_key].upper(),
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#3498db"
            )
            lbl_depto.pack(pady=(15, 5), fill="x")

            if not cola.items:
                lbl_vacio = ctk.CTkLabel(
                    self.scroll_sala, 
                    text="Vacio",
                    font=ctk.CTkFont(size=12, slant="italic"),
                    text_color="gray"
                )
                lbl_vacio.pack(pady=5, fill="x")
            else:
                for p in cola.items:
                    color = "#c0392b" if p.prioridad == 1 else "#34495e"
                    # Usamos el método __str__ del modelo para mostrar si es reserva o emergencia
                    p_text = str(p)
                    
                    p_label = ctk.CTkLabel(
                        self.scroll_sala, 
                        text=p_text,
                        fg_color=color,
                        corner_radius=5,
                        padx=10,
                        width=280,
                        height=30,
                        anchor="w"
                    )
                    p_label.pack(pady=2, padx=10)

    def mostrar_historico(self):
        """Abre una ventana secundaria para visualizar todos los pacientes atendidos."""
        vent_hist = ctk.CTkToplevel(self)
        vent_hist.title("Histórico de Atenciones")
        vent_hist.geometry("500x600")
        vent_hist.attributes('-topmost', True)

        ctk.CTkLabel(
            vent_hist, 
            text="Pacientes Atendidos", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)
        
        scroll_hist = ctk.CTkScrollableFrame(vent_hist, width=450, height=450)
        scroll_hist.pack(pady=10, padx=20, fill="both", expand=True)

        if not self.hospital.historial:
            ctk.CTkLabel(
                scroll_hist, 
                text="No hay registros historicos todavia.", 
                font=ctk.CTkFont(slant="italic")
            ).pack(pady=20)
        else:
            for p in reversed(self.hospital.historial):
                frame_p = ctk.CTkFrame(scroll_hist, fg_color="#2c3e50", corner_radius=8)
                frame_p.pack(pady=5, padx=5, fill="x")
                
                depto_nom = self.DEPTOS_DISPLAY.get(p.departamento, p.departamento)
                info = f"{p.nombre}\nArea: {depto_nom}"
                
                ctk.CTkLabel(
                    frame_p, 
                    text=info, 
                    justify="left", 
                    anchor="w"
                ).pack(side="left", padx=10, pady=10)
                
                hora_str = time.strftime('%H:%M:%S', time.localtime(p.hora_atencion))
                ctk.CTkLabel(
                    frame_p, 
                    text=f"Atendido: {hora_str}", 
                    font=ctk.CTkFont(size=11), 
                    text_color="gray"
                ).pack(side="right", padx=10)

    def actualizar_estadisticas(self):
        """Actualiza los valores de atención y espera en el panel izquierdo."""
        total = self.hospital.total_atendidos()
        espera = self.hospital.tiempo_promedio_espera()
        self.lbl_atendidos.configure(text=f"Atendidos: {total}")
        self.lbl_espera.configure(text=f"Espera Promedio: {espera:.2f}s")

    def mostrar_reporte(self):
        """Genera un reporte detallado, lo muestra y lo guarda en la carpeta /data."""
        resumen = self.hospital.obtener_resumen_por_departamento()
        total_global = self.hospital.total_atendidos()
        espera_global = self.hospital.tiempo_promedio_espera()

        texto_reporte = "REPORTE DE EFICIENCIA HOSPITALARIA\n"
        texto_reporte += "="*35 + "\n"
        texto_reporte += f"Total General: {total_global} pacientes\n"
        texto_reporte += f"Espera Media Global: {espera_global:.2f}s\n\n"
        texto_reporte += "DESGLOSE POR DEPARTAMENTO:\n"
        texto_reporte += "-"*35 + "\n"
        
        for depto, datos in resumen.items():
            nombre = self.DEPTOS_DISPLAY.get(depto, depto)
            texto_reporte += f"• {nombre}:\n"
            texto_reporte += f"  - Atendidos: {datos['total']}\n"
            texto_reporte += f"  - Espera Promedio: {datos['promedio']:.2f}s\n\n"
        
        messagebox.showinfo("Reporte de Eficiencia", texto_reporte)
        
        try:
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(base, "data")
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            report_path = os.path.join(data_dir, "reporte_eficiencia.txt")

            with open(report_path, "w", encoding="utf-8") as f:
                f.write(texto_reporte)
            print(f"Reporte generado en: {report_path}")
        except Exception as e:
            print(f"Error al guardar reporte: {e}")


if __name__ == "__main__":
    app = AppMedica()
    app.mainloop()