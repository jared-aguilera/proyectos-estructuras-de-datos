"""
Gestion de departamentos y persistencia de datos del hospital.
"""

import json
import os
import time
from motor_medico import ColaPrioridad
from modelos import Paciente

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
        
        # Lista de pacientes con cita programada
        self.reservas = []

        # cargar datos si existen
        self.cargar_datos()

    def registrar_paciente(self, nombre, prioridad, departamento):
        # Primero validamos antes de hacer cualquier cosa
        es_valido, mensaje = self.validar_paciente(nombre)
        if not es_valido:
            return False, mensaje

        if departamento not in self.departamentos:
            return False, "Departamento no valido."

        paciente = Paciente(nombre, prioridad, departamento)
        self.departamentos[departamento].enqueue(paciente)
        self.guardar_datos()
        return True, "Registro exitoso"

    def registrar_reserva(self, nombre, departamento, hora_cita):
        """
        Registra una cita para una hora específica validando que sea en el futuro.
        """
        es_valido, mensaje = self.validar_paciente(nombre)
        if not es_valido:
            return False, mensaje
            
        # Validación de hora futura
        hora_actual = time.strftime('%H:%M')
        if hora_cita <= hora_actual:
            return False, f"La hora {hora_cita} ya pasó. Elija una hora futura."

        # Creamos al paciente con prioridad Regular por defecto, pero con hora_cita
        paciente = Paciente(nombre, 2, departamento, hora_cita)
        self.reservas.append(paciente)
        self.guardar_datos()
        return True, f"Cita agendada para las {hora_cita}"

    def verificar_reservas(self):
        """Compara la hora actual con las reservas y las mueve a la cola activa."""
        hora_actual = time.strftime('%H:%M')
        pacientes_activados = []
        
        # Buscamos citas que coincidan con la hora actual
        for p in self.reservas[:]:
            if hora_actual >= p.hora_cita:
                # Al activarse, entra a la cola de su departamento
                # Le damos prioridad 2 (Regular) pero aparecerá al frente por tiempo
                self.departamentos[p.departamento].enqueue(p)
                self.reservas.remove(p)
                pacientes_activados.append(p.nombre)
        
        if pacientes_activados:
            self.guardar_datos()
            
        return pacientes_activados

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
            "reservas": [
                {
                    "nombre": p.nombre,
                    "departamento": p.departamento,
                    "hora_cita": p.hora_cita
                }
                for p in self.reservas
            ],
            "colas_activas": {
                depto: [
                    {
                        "nombre": p.nombre,
                        "prioridad": p.prioridad,
                        "departamento": p.departamento,
                        "hora_llegada": p.hora_llegada,
                        "hora_cita": getattr(p, "hora_cita", None)
                    }
                    for p in cola.items
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
                paciente = Paciente(p["nombre"], p["prioridad"], p["departamento"])
                paciente.hora_llegada = p["hora_llegada"]
                paciente.hora_atencion = p["hora_atencion"]
                self.historial.append(paciente)

            for r in datos.get("reservas", []):
                reserva = Paciente(r["nombre"], 2, r["departamento"], r["hora_cita"])
                self.reservas.append(reserva)

            colas_activas = datos.get("colas_activas", {})
            for depto, lista_pacientes in colas_activas.items():
                if depto in self.departamentos:
                    for p_data in lista_pacientes:
                        paciente = Paciente(
                            p_data["nombre"],
                            p_data["prioridad"],
                            p_data["departamento"],
                            p_data.get("hora_cita")
                        )
                        paciente.hora_llegada = p_data["hora_llegada"]
                        self.departamentos[depto].enqueue(paciente)
                        
        except:
            pass
        
    def validar_paciente(self, nombre):
        """Verifica que el nombre cumpla con las reglas del hospital."""
        if not nombre:
            return False, "El nombre no puede estar vacio."
        
        if not all(x.isalpha() or x.isspace() for x in nombre):
            return False, "El nombre solo debe contener letras."
            
        return True, "OK"
    
    def obtener_resumen_por_departamento(self):
        """Calcula el total de atendidos y espera promedio por cada area."""
        resumen = {}
        for depto in self.departamentos.keys():
            atendidos_depto = [p for p in self.historial if p.departamento == depto]
            total = len(atendidos_depto)
            
            espera_total = 0
            for p in atendidos_depto:
                espera_total += (p.hora_atencion - p.hora_llegada)
            
            promedio = espera_total / total if total > 0 else 0
            resumen[depto] = {"total": total, "promedio": promedio}
        return resumen