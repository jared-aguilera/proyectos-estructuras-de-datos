"""
Sistema de Gestión de Reservas de Hotel.
Este módulo maneja la lógica de reservaciones utilizando una pila personalizada.
"""

from modelos import Habitacion, Reserva
from pila import PilaPersonalizada


class MotorHotel:
    """
    Controlador principal para las operaciones del hotel.
    """

    def __init__(self):
        # Punto 2: Instanciar pilas con capacidad de 20
        self.pila_reservas_actuales = PilaPersonalizada(capacidad=20)
        self.pila_deshacer = PilaPersonalizada(capacidad=20)
        
        # Punto 4: Inicialización obligatoria de habitaciones
        self.habitaciones = [
            Habitacion(101, "Simple", 500.0),
            Habitacion(102, "Simple", 500.0),
            Habitacion(201, "Doble", 800.0),
            Habitacion(202, "Doble", 800.0),
            Habitacion(301, "Suite", 1500.0),
            Habitacion(302, "Suite", 1500.0)
        ]
        self.contador_reservas = 1

    def reservar_habitacion(self, habitacion, fecha, cliente):
        """
        Registra una nueva reserva validando la integridad de los datos.
        """
        # Validación: El objeto debe ser de tipo Habitacion (evita AttributeError)
        if not isinstance(habitacion, Habitacion):
            print("Error: el objeto habitacion no es valido.")
            return

        # Validación: El nombre debe ser texto y no estar vacío
        if not isinstance(cliente, str) or not cliente.strip():
            print("Error: el nombre del cliente debe ser texto.")
            return

        # Validación: Solo letras y espacios (bloquea símbolos y números)
        cliente_limpio = cliente.strip()
        if not cliente_limpio.replace(" ", "").isalpha():
            print("Error: el nombre del cliente solo debe contener letras.")
            return

        # Validación: La fecha no puede ser nula o solo espacios
        if not isinstance(fecha, str) or not fecha.strip():
            print("Error: la fecha no puede estar vacia.")
            return

        # Validación: Estado de la habitación
        if not habitacion.disponible:
            print(f"Error: La habitacion {habitacion.numero} no esta disponible.")
            return

        # Crear instancia de Reserva
        nueva_reserva = Reserva(
            self.contador_reservas, 
            habitacion, 
            fecha, 
            cliente_limpio
        )

        # Punto 3: Usar .push() en lugar de .append()
        self.pila_reservas_actuales.push(nueva_reserva)
        
        # Actualizar estado y limpiar historial de deshacer
        habitacion.disponible = False
        self.pila_deshacer = PilaPersonalizada(capacidad=20)

        self.contador_reservas += 1
        print("Reserva realizada correctamente")
        print(nueva_reserva)

    def cancelar_reserva(self):
        """
        Mueve la última reserva de la pila actual a la pila de deshacer.
        """
        # Punto 3: Usar .is_empty()
        if self.pila_reservas_actuales.is_empty():
            print("No hay reservas para cancelar.")
            return

        # Punto 3: Usar .pop()
        reserva = self.pila_reservas_actuales.pop()
        reserva.habitacion.disponible = True
        self.pila_deshacer.push(reserva)

        print(f"Reserva #{reserva.id_reserva} cancelada")

    def deshacer_cancelacion(self):
        """
        Recupera la última reserva cancelada.
        """
        if self.pila_deshacer.is_empty():
            print("No hay acciones para deshacer.")
            return

        reserva = self.pila_deshacer.pop()
        reserva.habitacion.disponible = False
        self.pila_reservas_actuales.push(reserva)

        print(f"Cancelacion deshecha: Reserva #{reserva.id_reserva}")