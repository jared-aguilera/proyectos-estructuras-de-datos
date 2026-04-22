import numpy as np
import random
import copy
import time
from .nodo import Nodo

class GeneticEngine:
    def __init__(self, p_crossover = 0.9, p_mutation = 0.1, tournament_size = 7):
        self.p_cross = p_crossover
        self.p_mut = p_mutation
        self.k = tournament_size
        # listas para controlar la aridad en las mutaciones
        self.f_binarias = ['+', '-', '*', '/']
        self.f_unitarias = ['sin', 'cos', 'log', 'sqrt', 'exp']

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
        """seleccion por torneo k = 7 [cite: 30, 38]"""
        indices = np.random.choice(len(poblacion), self.k, replace = False)
        #aqui buscamos el mejor MSE, el mejor fitness
        mejor_idx = indices[np.argmin([fitness_scores[i] for i in  indices])]
        return self.clonar_individuo(poblacion[mejor_idx])
    
    def cruce_subarboles(self, padre1, padre2):
        """intercambia subarboles entre dos padres """
        h1 = self.clonar_individuo(padre1)
        h2 = self.clonar_individuo(padre2)

        if random.random() < self.p_cross:
            nodos1 = self.obtener_todos_los_nodos(h1)
            nodos2 = self.obtener_todos_los_nodos(h2)

            p1 = random.choice(nodos1)
            p2 = random.choice(nodos2)

            # correccion de swap para no perder ramas y evitar ValueError [cite: 60]
            p1.valor, p2.valor = p2.valor, p1.valor
            p1.izquierda, p2.izquierda = p2.izquierda, p1.izquierda
            p1.derecha, p2.derecha = p2.derecha, p1.derecha

        return h1, h2
    
    def mutacion_punto(self, individuo, funciones, terminales):
        """cambia un nodo por otro dell mismo tipo respetando aridad [cite: 33]"""
        mutante = self.clonar_individuo(individuo)
        nodos = self.obtener_todos_los_nodos(mutante)
        target = random.choice(nodos)

        # si es operdaor binario cambia por otro binario
        if target.valor in self.f_binarias:
            target.valor = random.choice(self.f_binarias)
        # si es unitario por unitario para no dejar hijos en None
        elif target.valor in self.f_unitarias:
            target.valor = random.choice(self.f_unitarias)
        else:
            target.valor = random.choice(terminales)

        return mutante

    def mutacion_subarbol(self, individuo, poblador, funciones, terminales, max_depth=3):
        """reemplaza un subarbol completo por uno nuevo [cite: 34]"""
        mutante = self.clonar_individuo(individuo)
        nodos = self.obtener_todos_los_nodos(mutante)
        target = random.choice(nodos)

        # creamos un subarbol nuevo usando la clase de absalon [cite: 60]
        nuevo_sub = poblador.generar_arbol_recursivo(funciones, terminales, max_depth, method="grow")

        # inyeccion del nuevo subarbol
        target.valor = nuevo_sub.valor
        target.izquierda = nuevo_sub.izquierda
        target.derecha = nuevo_sub.derecha
        
        return mutante
    
    def aplicar_elitismo(self, poblacion, fitness_scores):
        """regresa una copia del mejor indivudo [cite: 35]"""
        mejor_idx = np.argmin(fitness_scores)
        return self.clonar_individuo(poblacion[mejor_idx])
    
    def ejecutar_evolucion(self, dataset_name, generaciones=50, tam_poblacion=500):
        """flujo principal que ahora emite progreso en tiempo real [cite: 27, 38]"""
        from src.utils.data_loader import DataLoader
        from src.models.population import Population
        
        start_time = time.time()
        
        # carga de datos de david
        loader = DataLoader()
        X, y = loader.cargar_dataset(dataset_name)
        
        funciones = self.f_binarias + self.f_unitarias
        # terminales: variables Xn y constantes aleatorias [-1, 1] [cite: 38]
        terminales = [f'X{i}' for i in range(X.shape[1])] + [round(random.uniform(-1, 1), 2)]
        
        # inicializacion ramped half-and-half (max depth 4) [cite: 28, 38]
        poblador = Population(tam_poblacion, max_depth_init=4)
        poblacion = poblador.create_population(funciones, terminales)
        
        evaluador = Evaluador()

        for gen in range(generaciones):
            # calculo de fitness (MSE) [cite: 29]
            scores = [evaluador.obtener_fitness(ind, X, y) for ind in poblacion]
            mejor_idx = np.argmin(scores)
            mejor_mse = scores[mejor_idx]
            mejor_individuo = poblacion[mejor_idx]
            
            # emitimos datos de la generacion para la terminal web
            yield {
                "gen": gen,
                "mse": float(mejor_mse),
                "formula": str(mejor_individuo)
            }
            
            nueva_poblacion = []
            # elitismo [cite: 35]
            nueva_poblacion.append(self.clonar_individuo(mejor_individuo))
            
            while len(nueva_poblacion) < tam_poblacion:
                # seleccion por torneo de 7 [cite: 30, 38]
                p1 = self.seleccion_torneo(poblacion, scores)
                p2 = self.seleccion_torneo(poblacion, scores)
                
                # cruce de subarboles con prob 0.9 [cite: 31, 38]
                h1, h2 = self.cruce_subarboles(p1, p2)
                
                # mutaciones (subarbol 0.1 y punto 0.05) [cite: 38]
                if random.random() < self.p_mut:
                    h1 = self.mutacion_subarbol(h1, poblador, funciones, terminales)
                if random.random() < 0.05:
                    h2 = self.mutacion_punto(h2, funciones, terminales)
                
                nueva_poblacion.extend([h1, h2])
            
            poblacion = nueva_poblacion[:tam_poblacion]
            
        total_time = round(time.time() - start_time, 4)
        yield {
            "final": True,
            "tiempo": total_time
        }
    
class Evaluador:
    def calcular_mse(self, y_real, y_predicho):
        """calcula el error cuadratico medio estandar con proteccion [cite: 29, 60]"""
        try:
            error = np.mean(np.square(y_real - y_predicho))
            return error if np.isfinite(error) else 1e15
        except:
            return 1e15

    def obtener_fitness(self, arbol, X, y_real):
        """conecta el arbol con el calculo de error"""
        y_predicho = arbol.evaluar(X)
        fitness = self.calcular_mse(y_real, y_predicho)
        return fitness