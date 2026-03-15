"""
Sistema de Gestión de Reservas de Hotel.
Este módulo maneja la lógica de reservaciones utilizando una pila personalizada.
"""

import json
import os
from datetime import datetime
from modelos import Habitacion, Reserva
from pila import PilaPersonalizada


class SistemaReservasHotel:
    """
    Controlador principal para las operaciones del hotel.
    """

    def __init__(self):
        self.pila_reservas_actuales = PilaPersonalizada(capacidad=20)
        self.pila_deshacer = PilaPersonalizada(capacidad=20)
        self.habitaciones = [
            Habitacion(101, "Simple", 500.0), Habitacion(102, "Simple", 500.0),
            Habitacion(201, "Doble", 800.0), Habitacion(202, "Doble", 800.0),
            Habitacion(301, "Suite", 1500.0), Habitacion(302, "Suite", 1500.0)
        ]
        self.contador_reservas = 1
        # Se intenta cargar datos automáticamente al iniciar el programa
        self.cargar_datos()

    def reservar_habitacion(self, cliente, fecha, tipo="Simple", noches=1):
        """
        Registra una nueva reserva validando la integridad de los datos.
        """
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except:
            return False

        if not isinstance(cliente, str) or not cliente.strip():
            return False

        cliente_limpio = cliente.strip()
        if not cliente_limpio.replace(" ", "").isalpha():
            return False

        for habitacion in self.habitaciones:
            if habitacion.tipo == tipo and habitacion.disponible:
                
                nueva_reserva = Reserva(
                    self.contador_reservas, habitacion, fecha, cliente_limpio, noches
                )

                self.pila_reservas_actuales.push(nueva_reserva)
                habitacion.disponible = False
                self.pila_deshacer = PilaPersonalizada(capacidad=20)
                self.contador_reservas += 1
                
                self.guardar_datos() # Guardado automático
                return True
        return False

    def cancelar_reserva(self, id_reserva=None):
        """
        Mueve la última reserva de la pila actual a la pila de deshacer.
        """
        if self.pila_reservas_actuales.is_empty():
            return False
        reserva = self.pila_reservas_actuales.pop()
        reserva.habitacion.disponible = True
        self.pila_deshacer.push(reserva)
        self.guardar_datos() # Guardado automático al cancelar
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
        self.guardar_datos() # Guardado automático al deshacer
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
    
    def buscar_reservas(self, criterio, valor):
        """
        Busca reservas en la pila actual por cliente, fecha o número de habitación.
        Retorna una lista con las coincidencias encontradas.
        """
        resultados = []
        criterio = criterio.lower()
        
        # Iteramos sobre los elementos de la pila de reservas actuales
        for reserva in self.pila_reservas_actuales.elementos:
            if criterio == "cliente" and valor.lower() in reserva.cliente.lower():
                resultados.append(reserva)
            elif criterio == "fecha" and valor == reserva.fecha:
                resultados.append(reserva)
            elif criterio == "habitación" and str(valor) == str(reserva.habitacion.numero):
                resultados.append(reserva)
                
        return resultados
    
    def guardar_datos(self):
        """Guarda automáticamente en unidad2_sistema_reservas/data/reservas.json."""
        
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_path, "data")
        file_path = os.path.join(data_dir, "reservas.json")

        # Creamos la carpeta data si no existe dentro de unidad2
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        datos = {
            "contador": self.contador_reservas,
            "habitaciones": [{"numero": h.numero, "disponible": h.disponible} for h in self.habitaciones],
            "reservas": [
                {
                    "id": r.id_reserva, 
                    "cliente": r.cliente, 
                    "fecha": r.fecha, 
                    "noches": r.noches, # Aseguramos que se guarde el dato de noches
                    "hab_numero": r.habitacion.numero
                } for r in self.pila_reservas_actuales.elementos
            ]
        }
        with open(file_path, "w") as f:
            json.dump(datos, f, indent=4)

    def cargar_datos(self):
        """Carga los datos desde la carpeta data de la unidad 2."""
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_path, "data", "reservas.json")

        if not os.path.exists(file_path):
            return
        
        try:
            with open(file_path, "r") as f:
                datos = json.load(f)
            
            self.contador_reservas = datos["contador"]
            for h_info in datos["habitaciones"]:
                hab = self.buscar_habitacion(h_info["numero"])
                if hab:
                    hab.disponible = h_info["disponible"]
            
            self.pila_reservas_actuales.elementos = []
            for r_info in datos["reservas"]:
                hab = self.buscar_habitacion(r_info["hab_numero"])
                # Recuperamos las noches del JSON, si no existen por error, ponemos 1
                noches_recuperadas = r_info.get("noches", 1)
                nueva_r = Reserva(
                    r_info["id"], 
                    hab, 
                    r_info["fecha"], 
                    r_info["cliente"], 
                    noches_recuperadas
                )
                self.pila_reservas_actuales.push(nueva_r)
        except Exception:
            pass