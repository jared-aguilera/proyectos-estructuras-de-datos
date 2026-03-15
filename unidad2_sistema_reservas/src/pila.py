class PilaPersonalizada:
    """
    Clase que representa una estructura de datos tipo pila con capacidad limitada
    """
    def __init__(self, capacidad):
        self.elementos =[] # Lista donde guardamos todo
        self.capacidad_maxima = capacidad

    def is_empty(self):
        """Verifica si la pila no contiene elementos"""
        return len(self.elementos) == 0 
    def is_full(self):
        """Verifica si la pila ha alcanzado su capacidad maxima"""
        return len(self.elementos) >= self.capacidad_maxima
    
    def push(self, elemento):
        # Si ya esta llena soltamos el error de overflow
        if self.is_full():
            raise OverflowError("La pila esta llena")
        self.elementos.append(elemento)
        return True
    
    def pop(self):
        """
        Elimina y retorna el elemento en el tope de la pila
        
        """
        if self.is_empty():
            raise IndexError("La pila esta vacia")
        return self.elementos.pop()
    
    def peek(self):
        """
        Retorna el elemento en el tope sin eliminarlo
        """
        if self.is_empty():
            raise IndexError("No se puede hacer peek ya que la pila esta vacia")
        return self.elementos[-1]
    
    def size(self):
        """Retorna la cantidad actual de elementos en la pila"""
        return len(self.elementos)
    
    def __str__(self):
        # Esto es para que la lista se imprima como texto entendible
        return str([str(e) for e in self.elementos])