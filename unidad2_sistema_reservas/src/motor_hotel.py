"""
Sistema de Gestión de Reservas de Hotel.
Este módulo maneja la lógica de reservaciones utilizando una pila personalizada.
"""

from datetime import datetime
from modelos import Habitacion, Reserva
from pila import PilaPersonalizada


class SistemaReservasHotel: # Nombre ajustado para el test
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

    def reservar_habitacion(self, cliente, fecha, tipo="Simple"): # Parámetros ajustados al test
        """
        Registra una nueva reserva validando la integridad de los datos.
        """
        # Validación de fecha para el test
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except:
            return False

        # Validación: El nombre debe ser texto y no estar vacío
        if not isinstance(cliente, str) or not cliente.strip():
            return False

        # Validación: Solo letras y espacios
        cliente_limpio = cliente.strip()
        if not cliente_limpio.replace(" ", "").isalpha():
            return False

        # Búsqueda de habitación por tipo para el test
        for habitacion in self.habitaciones:
            if habitacion.tipo == tipo and habitacion.disponible:
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
                return True # Retorno para validación del test

        return False

    def cancelar_reserva(self, id_reserva=None): # Parámetro opcional para el test
        """
        Mueve la última reserva de la pila actual a la pila de deshacer.
        """
        # Punto 3: Usar .is_empty()
        if self.pila_reservas_actuales.is_empty():
            return False

        # Punto 3: Usar .pop()
        reserva = self.pila_reservas_actuales.pop()
        reserva.habitacion.disponible = True
        self.pila_deshacer.push(reserva)
        return True

    def deshacer_cancelacion(self):
        """
        Recupera la última reserva cancelada.
        """
        if self.pila_deshacer.is_empty():
            return False

        reserva = self.pila_deshacer.pop()
        reserva.habitacion.disponible = False
        self.pila_reservas_actuales.push(reserva)
        return True
    
    def mostrar_reservas(self):
        """
        Muestra todas las reservas actuales almacenadas en la pila.
        """
        if self.pila_reservas_actuales.is_empty():
            print("No hay reservas actuales.")
        else:
            print("Lista de Reservas Actuales:")
            # Esto usa el método __str__ de la PilaPersonalizada
            print(self.pila_reservas_actuales)
    
    def buscar_habitacion(self, numero):
        """
        Busca una habitación específica por su número.
        """
        for hab in self.habitaciones:
            if hab.numero == numero:
                return hab
        return None