import numpy as np
import random
import copy
from .nodo import Nodo

class GeneticEngine:
    def __init__(self, p_crossover = 0.9, p_mutation = 0.1, tournament_size = 7):
        self.p_cross = p_crossover
        self.p_mut = p_mutation
        self.k = tournament_size

    #aqui trabajamos con el codigo de miguelito
    def clonar_individuo(self, nodo):
        """copiar profundidad de una arbol de miguel"""
        if nodo is None: return None
        izq = self.clonar_individuo(nodo.izquierda)
        der = self.clonar_individuo(nodo.derecha)
        return Nodo(nodo.valor, izq, der)
    
    def obtener_todos_los_nodos(self, nodo):
        """lista todas las referencias a los nodos"""
        nodos = [nodo]
        if nodo.izquierda:
            nodos.extend(self.obtener_todos_los_nodos(nodo.izquierda))
        if nodo.derecha:
            nodos.extend(self.obtener_todos_los_nodos(nodo.derecha))
        return nodos
        
    #operadores genericos
    def seleccion_torneo(self, poblacion, fitness_scores):
        """seleccion por torneo k = 7"""
        indices = np.random.choice(len(poblacion), self.k, replace = False)
        #aqui buscamos el mejor MSE, el mejor fitness
        mejor_idx = indices[np.argmin([fitness_scores[i] for i in  indices])]
        return self.clonar_individuo(poblacion[mejor_idx])
    
    def cruce_subarboles(self, padre1, padre2):
        """intercambia subarboles entre dos padres"""
        h1 = self.clonar_individuo(padre1)
        h2 = self.clonar_individuo(padre2)

        if random.random() < self.p_cross:
            nodos1 = self.obtener_todos_los_nodos(h1)
            nodos2 = self.obtener_todos_los_nodos(h2)

            p1 = random.choice(nodos1)
            p2 = random.choice(nodos2)

            #swap de contenidos
            p1.valor, p2.valor = p2.valor, p1.valor
            p1.izquierda, p2.izquierda = p2.izquierda, p1.izquierda
            p1.derecha, p2.derecha = p2.derecha, p1.derecha

        return h1, h2
    
    def mutacion_punto(self, individuo, funciones, terminales):
        """cambia un nodo por otro dell mismo tipo"""
        mutante = self.clonar_individuo(individuo)
        nodos = self.obtener_todos_los_nodos(mutante)
        target = random.choice(nodos)

        #si es operdaor cambia por otro operador
        if target.valor in funciones:
            target.valor = random.choice(funciones)
        #si es terminal, cambia por otro terminal
        else:
            target.valor = random.choice(terminales)

        return mutante
    
    def aplicar_elitismo(self, poblacion, fitness_scores):
        """regresa una copia del mejor indivudo"""
        mejor_idx = np.argmin(fitness_scores)
        return self.clonar_individuo(poblacion[mejor_idx])

class Evaluador:
    def calcular_mse(self, y_real, y_predicho):
        """calcula el error cuadratico medio estandar"""
        mse = np.mean((y_real - y_predicho)**2)
        return mse

    def obtener_fitness(self, arbol, X, y_real):
        """conecta el arbol con el calculo de error"""
        y_predicho = arbol.evaluar(X)
        fitness = self.calcular_mse(y_real, y_predicho)
        return fitness