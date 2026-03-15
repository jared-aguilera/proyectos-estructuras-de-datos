"""
Gestion de departamentos y persistencia de datos del hospital.
"""

import json
import os
import time
from motor_medico import Paciente, ColaPrioridad


class GestionHospital:

    def __init__(self):

        # Diccionario con una cola por departamento
        self.departamentos = {
            "urgencias": ColaPrioridad(),
            "pediatria": ColaPrioridad(),
            "medicina_general": ColaPrioridad()
        }

        # historial de pacientes atendidos
        self.historial = []

        # cargar datos si existen
        self.cargar_datos()

    def registrar_paciente(self, nombre, prioridad, departamento):

        if departamento not in self.departamentos:
            return False

        paciente = Paciente(
            nombre,
            prioridad,
            departamento
        )

        self.departamentos[departamento].enqueue(paciente)

        self.guardar_datos()

        return True


    def atender_paciente(self, departamento):

        if departamento not in self.departamentos:
            return None

        cola = self.departamentos[departamento]

        if cola.peek() is None:
            return None

        paciente = cola.dequeue()

        paciente.hora_atencion = time.time()

        self.historial.append(paciente)

        self.guardar_datos()

        return paciente


    def total_atendidos(self):
        return len(self.historial)


    def ultimos_pacientes(self, departamento, limite=5):

        lista = []

        for p in self.historial:
            if p.departamento == departamento:
                lista.append(p)

        return lista[-limite:]


    def tiempo_promedio_espera(self):

        if not self.historial:
            return 0

        total = 0

        for p in self.historial:

            if hasattr(p, "hora_atencion"):
                total += (p.hora_atencion - p.hora_llegada)

        return total / len(self.historial)


    def guardar_datos(self):

        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base, "data")
        archivo = os.path.join(data_dir, "pacientes.json")

        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        datos = {
            "historial": [
                {
                    "nombre": p.nombre,
                    "prioridad": p.prioridad,
                    "departamento": p.departamento,
                    "hora_llegada": p.hora_llegada,
                    "hora_atencion": getattr(p, "hora_atencion", None)
                }
                for p in self.historial
            ],
            # Se guardan las colas activas por departamento
            "colas_activas": {
                depto: [
                    {
                        "nombre": p.nombre,
                        "prioridad": p.prioridad,
                        "departamento": p.departamento,
                        "hora_llegada": p.hora_llegada
                    }
                    for p in cola.items  # Accedemos a la deque
                ]
                for depto, cola in self.departamentos.items()
            }
        }

        with open(archivo, "w") as f:
            json.dump(datos, f, indent=4)


    def cargar_datos(self):

        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        archivo = os.path.join(base, "data", "pacientes.json")

        if not os.path.exists(archivo):
            return

        try:

            with open(archivo, "r") as f:
                datos = json.load(f)

            for p in datos.get("historial", []):

                paciente = Paciente(
                    p["nombre"],
                    p["prioridad"],
                    p["departamento"]
                )

                paciente.hora_llegada = p["hora_llegada"]
                paciente.hora_atencion = p["hora_atencion"]

                self.historial.append(paciente)

            # Cargamos las colas de espera (Pendientes)
            colas_activas = datos.get("colas_activas", {})
            for depto, lista_pacientes in colas_activas.items():
                if depto in self.departamentos:
                    for p_data in lista_pacientes:
                        paciente = Paciente(
                            p_data["nombre"],
                            p_data["prioridad"],
                            p_data["departamento"]
                        )
                        paciente.hora_llegada = p_data["hora_llegada"]
                        self.departamentos[depto].enqueue(paciente)
                        
        except:
            pass
