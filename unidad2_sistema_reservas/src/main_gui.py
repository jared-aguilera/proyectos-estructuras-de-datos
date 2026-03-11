import customtkinter as ctk
from tkinter import messagebox
from motor_hotel import SistemaReservasHotel

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AppHotel(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Reservas de Hotel - Gestión LIFO")
        self.geometry("1150x750")
        
        self.hotel = SistemaReservasHotel()
        
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_ui()
        self.update_ui()

    def setup_ui(self):
        # Panel Izquierdo: Visualización de habitaciones
        self.frame_habitaciones = ctk.CTkScrollableFrame(self, label_text="Panel de Disponibilidad")
        self.frame_habitaciones.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.frame_habitaciones.grid_columnconfigure((0, 1), weight=1)

        # Panel Derecho: Control
        self.frame_control = ctk.CTkFrame(self, width=350)
        self.frame_control.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # SECCIÓN 1: Buscador (Usa buscar_habitacion de motor_hotel)
        ctk.CTkLabel(self.frame_control, text="Búsqueda Rápida", font=("Arial", 16, "bold")).pack(pady=(10, 5))
        self.entry_busqueda = ctk.CTkEntry(self.frame_control, placeholder_text="Num. Habitación (ej. 101)")
        self.entry_busqueda.pack(fill="x", padx=20, pady=5)
        ctk.CTkButton(self.frame_control, text="🔍 Buscar", command=self.ejecutar_busqueda, fg_color="#5d6d7e").pack(fill="x", padx=20, pady=5)

        # SECCIÓN 2: Nueva Reserva
        ctk.CTkLabel(self.frame_control, text="Nueva Reserva", font=("Arial", 18, "bold")).pack(pady=(20, 10))
        self.entry_cliente = ctk.CTkEntry(self.frame_control, placeholder_text="Nombre del Cliente")
        self.entry_cliente.pack(fill="x", padx=20, pady=5)
        self.entry_fecha = ctk.CTkEntry(self.frame_control, placeholder_text="Fecha (YYYY-MM-DD)")
        self.entry_fecha.pack(fill="x", padx=20, pady=5)
        self.combo_tipo = ctk.CTkComboBox(self.frame_control, values=["Simple", "Doble", "Suite"])
        self.combo_tipo.pack(fill="x", padx=20, pady=5)
        self.btn_reservar = ctk.CTkButton(self.frame_control, text="Confirmar Reserva", command=self.ejecutar_reserva)
        self.btn_reservar.pack(fill="x", padx=20, pady=15)

        # SECCIÓN 3: Pila LIFO (Cancelar/Deshacer)
        ctk.CTkLabel(self.frame_control, text="Operaciones de Pila", font=("Arial", 16, "bold")).pack(pady=(10, 5))
        self.btn_cancelar = ctk.CTkButton(self.frame_control, text="Cancelar Última (Pop)", fg_color="#e74c3c", command=self.ejecutar_cancelacion)
        self.btn_cancelar.pack(fill="x", padx=20, pady=5)
        self.btn_deshacer = ctk.CTkButton(self.frame_control, text="Deshacer (Undo)", fg_color="#3498db", command=self.ejecutar_deshacer)
        self.btn_deshacer.pack(fill="x", padx=20, pady=5)

        # SECCIÓN 4: Historial Visual (Usa __str__ de PilaPersonalizada)
        ctk.CTkLabel(self.frame_control, text="Log de Pila Actual", font=("Arial", 14, "bold")).pack(pady=(15, 5))
        self.txt_log = ctk.CTkTextbox(self.frame_control, height=120, font=("Consolas", 11))
        self.txt_log.pack(fill="x", padx=15, pady=5)

    def ejecutar_busqueda(self):
        """Usa el método buscar_habitacion del motor."""
        try:
            num = int(self.entry_busqueda.get())
            hab = self.hotel.buscar_habitacion(num) #
            if hab:
                # Usa el __str__ de Habitacion definido en modelos.py
                messagebox.showinfo("Resultado", str(hab)) #
            else:
                messagebox.showwarning("No encontrado", f"La habitación {num} no existe.")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido.")

    def update_ui(self):
        for widget in self.frame_habitaciones.winfo_children():
            widget.destroy()

        for i, hab in enumerate(self.hotel.habitaciones):
            color_status = "#2ecc71" if hab.disponible else "#e74c3c"
            texto_status = "DISPONIBLE" if hab.disponible else "RESERVADA"
            
            card = ctk.CTkFrame(self.frame_habitaciones, border_width=2, border_color=color_status)
            card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkLabel(card, text=texto_status, text_color=color_status, font=("Arial", 12, "bold")).pack(pady=5)
            ctk.CTkLabel(card, text=f"Habitación {hab.numero}", font=("Arial", 18, "bold")).pack()
            ctk.CTkLabel(card, text=f"Tipo: {hab.tipo}").pack()
            
            # Botón de detalles: Muestra información si está reservada
            btn_info = ctk.CTkButton(card, text="Ver Detalles", width=100, height=20, 
                                     fg_color="transparent", border_width=1,
                                     command=lambda h=hab: self.mostrar_info_reserva(h))
            btn_info.pack(pady=10)

        # Actualiza el Log usando el __str__ de la Pila
        self.txt_log.delete("1.0", "end")
        if self.hotel.pila_reservas_actuales.is_empty():
            self.txt_log.insert("end", "Pila vacía...")
        else:
            self.txt_log.insert("end", str(self.hotel.pila_reservas_actuales))

        self.btn_cancelar.configure(state="normal" if not self.hotel.pila_reservas_actuales.is_empty() else "disabled")
        self.btn_deshacer.configure(state="normal" if not self.hotel.pila_deshacer.is_empty() else "disabled")

    def mostrar_info_reserva(self, hab):
        """Busca en la pila la reserva asociada a esa habitación."""
        if hab.disponible:
            messagebox.showinfo("Info", f"Habitación {hab.numero} está lista para recibir clientes.")
        else:
            # Buscamos en los elementos de la pila de Absalón
            for reserva in self.hotel.pila_reservas_actuales.elementos: #
                if reserva.habitacion.numero == hab.numero:
                    # Usa el __str__ de Reserva definido en modelos.py
                    messagebox.showinfo("Detalle de Reserva", str(reserva)) #
                    return

    def ejecutar_reserva(self):
        cliente, fecha, tipo = self.entry_cliente.get(), self.entry_fecha.get(), self.combo_tipo.get()
        if self.hotel.reservar_habitacion(cliente, fecha, tipo):
            messagebox.showinfo("Éxito", "¡Reserva en Pila!")
            self.update_ui()
        else:
            messagebox.showerror("Error", "No se pudo reservar.")

    def ejecutar_cancelacion(self):
        if self.hotel.cancelar_reserva():
            self.update_ui()

    def ejecutar_deshacer(self):
        if self.hotel.deshacer_cancelacion():
            self.update_ui()

if __name__ == "__main__":
    app = AppHotel()
    app.mainloop()