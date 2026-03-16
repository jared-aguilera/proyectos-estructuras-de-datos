import time

class Paciente:
    """
    Representa a un paciente dentro del sistema hospitalario.
    """
    def __init__(self, nombre, prioridad, departamento, hora_cita=None):
        self.nombre = nombre
        self.prioridad = prioridad
        self.departamento = departamento
        self.hora_llegada = time.time()
        self.hora_atencion = None
        self.hora_cita = hora_cita # Almacena la hora pactada (HH:MM)

    def __str__(self):
        tipo = "EMERGENCIA" if self.prioridad == 1 else "Regular"
        # Si tiene hora de cita, lo indicamos en su etiqueta visual
        if self.hora_cita:
            return f"[RESERVA {self.hora_cita}] {self.nombre}"
        return f"[{tipo}] {self.nombre}"