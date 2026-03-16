import time
from collections import deque

class Paciente:
    '''Representa a un paciente dentro del sistema'''
    def __init__(self, nombre, prioridad, departamento):
        self.nombre = nombre
        self.prioridad = prioridad
        self.departamento = departamento
        self.hora_llegada = time.time()
        self.hora_atencion = None

class ColaPrioridad:
    '''Gestiona dos colasa internas para priorizar emergencias sobre casos regulares'''
    def __init__(self):
        self.emergencias = deque()
        self.regulares = deque()
    def enqueue(self, paciente):
        '''añade a un paciente a la cola segun corresponda su prioridad'''
        if paciente.prioridad == 1:
            self.emergencias.append(paciente)
        else: self.regulares.append(paciente)
        
    def dequeue(self):
        '''extrae el siguiente paciente priorizando la cola de emergencia'''
        if self.emergencias:
            paciente = self.emergencias.popleft()
        elif self.regulares:
            paciente = self.regulares.popleft()
        else:
            return None
        paciente.hora_atencion = time.time()
        return paciente
    def peek(self):
        '''devuelve el proximo paciente en salir sin removerlo de la cola'''
        if self.emergencias:
            return self.emergencias[0]
        if self.regulares:
            return self.regulares[0]
        return None
class SistemaAtencionMedica:
    '''coordina la atencion de pacientes a traves de multiples departamentos'''
    def __init__(self):
        self.departamentos= {}
        self.tiempos_espera = []

    def agregar_paciente(self, nombre, prioridad, departamento):
        '''registra a un nuevo paciente en el departamento que debe ir'''
        if departamento not in self.departamentos:
            self.departamentos[departamento] = ColaPrioridad()
        paciente = Paciente(nombre, prioridad, departamento)
        self.departamentos[departamento].enqueue(paciente)
    
    def atender_paciente(self, departamento):
        '''procesa la atencion del siguiente paciente y registra sus estadisticas'''
        if departamento in self.departamentos:
            paciente = self.departamentos[departamento].dequeue()
            if paciente:
                espera = paciente.hora_atencion - paciente.hora_llegada
                self.tiempos_espera.append(espera)
                return paciente
            return None
    def obtener_promedio_espera(self):
        '''calcula el tiempo de espera para los pacientes'''
        if not self.tiempos_espera:
            return 0
        return sum(self.tiempos_espera) / len(self.tiempos_espera)