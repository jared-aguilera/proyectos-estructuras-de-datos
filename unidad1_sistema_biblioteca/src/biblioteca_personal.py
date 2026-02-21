class bibliotecaPersonal:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self._cantidad = 0

    def vacia(self):
        return self.cabeza is None
    def cantidad(self):
        return self._cantidad
    

    def insertar_inicio(self, libro):
        nuevo = nodoLibro(libro)
        if self.vacia():
            self.cabeza = self.cola = nuevo
        else:
            nuevo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo
            self.cabeza = nuevo
        self._cantidad += 1

    def insertar_final(self, libro):
        nuevo = nodoLibro(libro)
        if self.vacia():
            self.cabeza = self.cola = nuevo
        else:
            nuevo.anterior = self.cola
            self.cola.siguiente = nuevo
            self.cola = nuevo
        self._cantidad += 1

    def insertar_ordenado(self, libro):
        nuevo = nodoLibro(libro)

        if self.vacia():
            self.cabeza = self.cola = nuevo
            self._cantidad += 1
            return
        actual = self.cabeza
        while actual and actual.libro.titulo.lower() < libro.titulo.lower():
            actual = actual.siguiente
        if actual == self.cabeza:
            self.insertar_inicio(libro)
        elif actual is None:
            self.insertar_final(libro)
        else:
            anterior = actual.anterior
            anterior.siguiente = nuevo
            nuevo.anterior = anterior
            nuevo.siguiente = actual
            actual.anterior = nuevo
            self._cantidad += 1

    '''Consulta'''
    def buscar_isbn(self, isbn):
        actual = self.cabeza
        while actual:
            if actual.libro.isbn == isbn:
                return actual.libro
            actual = actual.siguiente
        return None

    def buscar_autor(self, autor):
        resultados = []
        actual = self.cabeza
        while actual:
            if actual.libro.autor.lower() == autor.lower():
                resultados.append(actual.libro)
            actual = actual.siguiente
        return resultados

    def buscar_categoria(self, categoria):
        resultados = []
        actual = self.cabeza
        while actual:
            if actual.libro.categoria.lower() == categoria.lower():
                resultados.append(actual.libro)
            actual = actual.siguiente
        return resultados
    
    '''actualiozar'''
    def actualizar_libro(self, isbn, titulo, autor, fecha, categoria):
        actual = self.cabeza
        while actual:
            if actual.libro.isbn == isbn:
                actual.libro.actualizar(titulo, autor, fecha, categoria)
                return True
            actual = actual.siguiente
        return False
    
    '''eliminar'''
    def eliminar_isbn(self, isbn):
        actual = self.cabeza
        while actual:
            if actual.libro.isbn == isbn:
                if actual.anterior:
                    actual.anterior.siguiente = actual.siguiente
                else:
                    self.cabeza = actual.siguiente
                if actual.siguiente:
                    actual.siguiente.anterior = actual.anterior
                else:
                    self.cola = actual.anterior
                self._cantidad -= 1
                return True
            actual = actual.siguiente
        return False

    def __iter__(self):
        actual = self.cabeza
        while actual:
            yield actual.libro
            actual = actual.siguiente
