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