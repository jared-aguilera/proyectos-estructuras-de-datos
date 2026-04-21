import numpy as np
import random
from .nodo import Nodo

class Population:
    def __init__(self, size, max_depth_init):
        self.size = size
        self.max_depth_init = max_depth_init
        self.invididuals = []

    def generar_arbol_recursivo(self, funciones, terminales, depth, method = "grow"):
        #condicion e parada: prfundidad 0 o azar en modo 'grow'
        if depth <= 0 or (method =="grow" and random.random() < 0.15):
            val = random.choice(terminales)

        #seleccionar funcion
        func = random.choice(funciones)

        #operadores binarios(requieren izq y der)
        if func in [ '+', '-', '*', '/']:
            izq = self.generar_srbol_recursivo(funciones, terminales, depth - 1, method)
            der = self.generar_srbol_recursivo(funciones, terminales, depth - 1, method)
            return Nodo(func, izq, der)
        #operadores unitarios(solo izq)
        else:
            izq = self.generar_arbol_recursivo(funciones, terminales, depth - 1, method)
            return Nodo(func, izq)
        
    def create_population(self, funciones, terminales):
        """Implementacion de Ramped Half-and-Half"""
        self.individuals = []
        half = self.size // 2

        for i in range(self.size):
            #alternar entre full y grow
            metodo = "full" if i < half else 'grow'
            #variar la profundidad inicial
            depth = random.randint(2, self.max_depth_init)

            nuevo_individuo = self.generar_arbol_recursivo(funciones, terminales, depth, metodo)
            self.individuals.append(nuevo_individuo)

        return self.individuals