<<<<<<< Updated upstream
=======
import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
from motor_hotel import SistemaReservasHotel

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AppHotel(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Reservas de Hotel")
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

        # SECCIÓN 1: Buscador Dinámico
        ctk.CTkLabel(self.frame_control, text="Búsqueda Rápida", font=("Arial", 16, "bold")).pack(pady=(10, 5))
        
        self.combo_criterio = ctk.CTkComboBox(
            self.frame_control, 
            values=["Habitación", "Cliente", "Fecha"],
            state="readonly",
            command=self.actualizar_interfaz_busqueda 
        )
        self.combo_criterio.set("Habitación")
        self.combo_criterio.pack(fill="x", padx=20, pady=2)

        # Este contenedor reserva el espacio entre el selector y el botón
        self.frame_input_busqueda = ctk.CTkFrame(self.frame_control, fg_color="transparent")
        self.frame_input_busqueda.pack(fill="x", padx=20, pady=5)

        self.entry_busqueda = ctk.CTkEntry(self.frame_input_busqueda, placeholder_text="Término a buscar...")
        self.entry_busqueda.pack(fill="x")

        self.cal_busqueda = DateEntry(self.frame_input_busqueda, background='darkblue', 
                                    foreground='white', borderwidth=2, date_pattern='y-mm-dd',
                                    state="readonly")
        
        ctk.CTkButton(self.frame_control, text="Buscar", command=self.ejecutar_busqueda, fg_color="#5d6d7e").pack(fill="x", padx=20, pady=5)
        

        # SECCIÓN 2: Nueva Reserva
        ctk.CTkLabel(self.frame_control, text="Nueva Reserva", font=("Arial", 18, "bold")).pack(pady=(20, 10))
        self.entry_cliente = ctk.CTkEntry(self.frame_control, placeholder_text="Nombre del Cliente")
        self.entry_cliente.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(self.frame_control, text="Seleccione Fecha:", font=("Arial", 12)).pack()
        # mindate=datetime.today() bloquea los días pasados 
        self.cal_reserva = DateEntry(self.frame_control, width=12, background='gray20', 
                                    foreground='white', borderwidth=2, 
                                    date_pattern='y-mm-dd', mindate=datetime.today(),
                                    state="readonly") # Evita que escriban la fecha manualmente
        self.cal_reserva.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(self.frame_control, text="Número de Noches:").pack()
        self.entry_noches = ctk.CTkEntry(self.frame_control, placeholder_text="1")
        self.entry_noches.insert(0, "1") # Valor por defecto
        self.entry_noches.pack(fill="x", padx=20, pady=5)

        self.combo_tipo = ctk.CTkComboBox(self.frame_control, values=["Simple", "Doble", "Suite"], 
                                        state="readonly") # Evita que escriban tipos inexistentes
        self.combo_tipo.set("Tipo de Habitación")
        self.combo_tipo.pack(fill="x", padx=20, pady=5)
        self.btn_reservar = ctk.CTkButton(self.frame_control, text="Confirmar Reserva", command=self.ejecutar_reserva)
        self.btn_reservar.pack(fill="x", padx=20, pady=15)

        # SECCIÓN 3: Pila
        ctk.CTkLabel(self.frame_control, text="Operaciones de la Pila", font=("Arial", 16, "bold"),).pack(pady=(10, 5))
        self.btn_cancelar = ctk.CTkButton(self.frame_control, text="Cancelar Última", fg_color="#e74c3c",text_color="black", command=self.ejecutar_cancelacion)
        self.btn_cancelar.pack(fill="x", padx=20, pady=5)
        self.btn_deshacer = ctk.CTkButton(self.frame_control, text="Deshacer", fg_color="#3498db", text_color="black", command=self.ejecutar_deshacer)
        self.btn_deshacer.pack(fill="x", padx=20, pady=5)

        # SECCIÓN 4: Historial Visual (Usa __str__ de PilaPersonalizada)
        ctk.CTkLabel(self.frame_control, text="Log de la Pila", font=("Arial", 14, "bold")).pack(pady=(15, 5))
        self.txt_log = ctk.CTkTextbox(self.frame_control, height=120, font=("Consolas", 11))
        self.txt_log.pack(fill="x", padx=15, pady=5)    
        
    def actualizar_interfaz_busqueda(self, seleccion):
        """Intercambia los widgets dentro del contenedor reservado."""
        if seleccion == "Fecha":
            self.entry_busqueda.pack_forget()
            self.cal_busqueda.pack(fill="x") # Se muestra arriba del botón Buscar
        else:
            self.cal_busqueda.pack_forget()
            self.entry_busqueda.pack(fill="x")
        
    def ejecutar_busqueda(self):
        """Ejecuta la búsqueda multi-criterio usando el motor."""
        criterio = self.combo_criterio.get()
        
        # Si es Fecha, se lee del calendario; si no, del cuadro de texto
        if criterio == "Fecha":
            valor = self.cal_busqueda.get()
        else:
            valor = self.entry_busqueda.get().strip()
            # Validamos que no esté vacío solo para texto
            if not valor:
                messagebox.showwarning("Atención", f"Por favor, ingrese un {criterio} para buscar.")
                return

        # Llamamos al método del motor que ya tenemos listo
        resultados = self.hotel.buscar_reservas(criterio, valor)
        
        if resultados:
            # Mostramos la info usando el __str__ de Reserva de Miguel
            mensaje = "\n\n".join([str(r) for r in resultados])
            messagebox.showinfo(f"Resultados para {criterio}: {valor}", mensaje)
        else:
            messagebox.showinfo("Búsqueda", f"No se encontraron reservas por {criterio} con: {valor}")
    
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
            # Buscamos en los elementos de la pila
            for reserva in self.hotel.pila_reservas_actuales.elementos: #
                if reserva.habitacion.numero == hab.numero:
                    # Usa el __str__ de Reserva definido en modelos.py
                    messagebox.showinfo("Detalle de Reserva", str(reserva)) #
                    return

    def ejecutar_reserva(self):
        cliente = self.entry_cliente.get()
        tipo = self.combo_tipo.get()
        fecha = self.cal_reserva.get() 
        
        # Obtener noches y convertir a entero
        try:
            noches_val = int(self.entry_noches.get())
        except ValueError:
            messagebox.showerror("Error", "El número de noches debe ser un número entero.")
            return

        # Ahora pasamos el valor de noches al motor
        if self.hotel.reservar_habitacion(cliente, fecha, tipo, noches_val):
            messagebox.showinfo("Éxito", f"Reserva de {noches_val} noches confirmada.")
            self.entry_cliente.delete(0, 'end')
            self.update_ui()
        else:
            messagebox.showerror("Error", "No se pudo realizar la reserva.")

    def ejecutar_cancelacion(self):
        if self.hotel.cancelar_reserva():
            self.update_ui()

    def ejecutar_deshacer(self):
        if self.hotel.deshacer_cancelacion():
            self.update_ui()

if __name__ == "__main__":
    app = AppHotel()
    app.mainloop()
>>>>>>> Stashed changes
