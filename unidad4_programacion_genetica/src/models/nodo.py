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

        # proteccion contra aridad incorrecta (si falta un hijo por mutacion)
        if der_val is None and self.valor in ['+', '-', '*', '/']:
            return izq_val if izq_val is not None else 0.0

        try:
            if self.valor == '+':
                res = izq_val + der_val
            elif self.valor == '-':
                res = izq_val - der_val
            elif self.valor == '*':
                res = izq_val * der_val
            elif self.valor == '/':
                # proteccion oficial del pdf: si |b| < 1e-10 regresa 1.0 [cite: 23]
                condicion = np.abs(der_val) < 1e-10
                res = np.where(condicion, 1.0, izq_val / np.where(condicion, 1.0, der_val))
            elif self.valor == 'sin':
                res = np.sin(izq_val)
            elif self.valor == 'cos':
                res = np.cos(izq_val)
            elif self.valor == 'log':
                # proteccion oficial: log(|x|) y evitar log(0) [cite: 24]
                val_abs = np.abs(izq_val)
                res = np.log(np.where(val_abs < 1e-10, 1.0, val_abs))
            elif self.valor == 'sqrt':
                # proteccion oficial: usar valor absoluto [cite: 25]
                res = np.sqrt(np.abs(izq_val))
            elif self.valor == 'exp':
                # proteccion extra: evitar que exp explote a infinito
                res = np.exp(np.clip(izq_val, -100, 100))
            else:
                return 0.0
            
            # limpieza de NaNs e Infs para que el MSE no sea 'nan' [cite: 60]
            return np.nan_to_num(res, nan=0.0, posinf=1e10, neginf=-1e10)
            
        except:
            return np.zeros(X.shape[0])

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

    def __str__(self):
        """representacion de la formula para el dashboard [cite: 48]"""
        if self.izquierda is None and self.derecha is None:
            return str(self.valor)
        if self.derecha is None:
            return f"{self.valor}({self.izquierda})"
        return f"({self.izquierda} {self.valor} {self.derecha})"