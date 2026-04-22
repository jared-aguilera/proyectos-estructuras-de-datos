import numpy as np

class Nodo:
    def __init__(self, valor, izquierda = None, derecha = None):
        self.valor = valor
        self.izquierda = izquierda
        self.derecha = derecha

    def evaluar(self, X):
        if self.izquierda is None and self.derecha is None:
            if isinstance(self.valor, str) and self.valor.startswith('X'):
                return X[:, int(self.valor[1:])]
            return self.valor
        
        izq_val = self.izquierda.evaluar(X) if self.izquierda else None
        der_val = self.derecha.evaluar(X) if self.derecha else None

        if self.valor == '+':
            return izq_val + der_val
        elif self.valor == '-':
            return izq_val - der_val
        elif self.valor == '*':
            return izq_val * der_val
        elif self.valor == '/':
            condicion = np.abs(der_val) < 1e-10
            der_val_seguro = np.where(condicion, 1.0, der_val)
            resultado = izq_val / der_val_seguro
            return np.where(condicion, 1.0, resultado)
        elif self.valor == 'sin':
            return np.sin(izq_val)
        elif self.valor == 'cos':
            return np.cos(izq_val)
        elif self.valor == 'log':
            val_abs = np.abs(izq_val)
            val_seguro = np.where(val_abs == 0, 1e-10, val_abs)
            return np.log(val_seguro)
        elif self.valor == 'sqrt':
            return np.sqrt(np.abs(izq_val))
        elif self.valor == 'exp':
            return np.exp(izq_val)

    def obtener_profundidad(self):
        izq_prof = self.izquierda.obtener_profundidad() if self.izquierda else 0
        der_prof = self.derecha.obtener_profundidad() if self.derecha else 0
        return 1 + max(izq_prof, der_prof)

    def contar_nodos(self):
        conteo = 1 
        if self.izquierda:
            conteo += self.izquierda.contar_nodos()
        if self.derecha:
            conteo += self.derecha.contar_nodos()
        return conteo