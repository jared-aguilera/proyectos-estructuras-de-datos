import time

class Paciente:
    def __init__(self, nombre, prioridad, departamento):
        self.nombre = nombre
        self.prioridad = prioridad
        self.departamento = departamento
        self.hora_llegada = time.time()
        self.hora_atencion = None
    def __str__(self):
        tipo = "EMERGENCIA" if self.prioridad == 1 else "Regular"
        return f"[{tipo}] {self.nombre}"