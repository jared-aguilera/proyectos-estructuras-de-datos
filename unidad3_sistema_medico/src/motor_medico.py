import time
from collections import deque
from .modelos import Paciente

class ColaPrioridad:
    '''Gestiona dos colasa internas para priorizar emergencias sobre casos regulares'''
    def __init__(self):
        self.emergencias = deque()
        self.regulares = deque()
    @property
    def items(self):
        return list(self.emergencias) + list(self.regulares)
    
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
