import numpy as np

class Evaluador:
    def calcular_mse(self, y_real, y_predicho):

        mse = np.mean((y_real - y_predicho)**2)
        return mse

    def obtener_fitness(self, arbol, X, y_real):

        y_predicho = arbol.evaluar(X)
        
        fitness = self.calcular_mse(y_real, y_predicho)
        
        return fitness