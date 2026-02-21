class bibliotecaPersonal: 
    """
    Gestiona una lista doblemente enlazada de libros
    que permite insertar buscar actualizar y eliminar libros
    """
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self._cantidad = 0

    def vacia(self): 
        """
        Indica si la lista esta vacia y
        va retornar true si no hay elementos
        """
        return self.cabeza is None
    
    def cantidad(self):
        '''retorna la cantidad de libros que se encuentran disponibles'''
        return self._cantidad
    
    def validar(self, libro):
        '''validaremos los datos de los libros,
        parametros seran libro objeto libro a validar
        lanzara valueError si algun dato es erroneo'''

        if not libro.isbn or not str(libro.isbn).strip().isdigit():
            raise ValueError("tu isbn es invalido")
        if not libro.titulo or not libro.titulo.strip():
            raise ValueError("titulo invalido")
        if not libro.autor or not libro.autor.strip():
            raise ValueError("autor invalido")
        if not str(libro.fecha).isdigit():
            raise ValueError("fecha invalida")
        if not libro.categoria or not libro.categoria.strip():
            raise ValueError("categoria invalida")
    
    def insertar_inicio(self, libro):
        '''insertara un libro al inicio de la lista
        lanzara valueError si el isbn ya existe o algun dato invalido'''

        self.validar(libro)
        if self.buscar_isbn(libro.isbn):
            raise ValueError("El isbn ya existe")
        nuevo = nodoLibro(libro)
        if self.vacia():
            self.cabeza = self.cola = nuevo
        else:
            nuevo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo
            self.cabeza = nuevo
        self._cantidad += 1

    def insertar_final(self, libro):
        '''insertara un libro al final de la lista'''

        self.validar(libro)
        if self.buscar_isbn(libro.isbn):
            raise ValueError("El isbn ya existe")
        nuevo = nodoLibro(libro)
        if self.vacia():
            self.cabeza = self.cola = nuevo
        else:
            nuevo.anterior = self.cola
            self.cola.siguiente = nuevo
            self.cola = nuevo
        self._cantidad += 1

    def insertar_ordenado(self, libro):
        '''insertara un libro de forma ordenada por titulo'''

        self.validar(libro)
        if self.buscar_isbn(libro.isbn):
            raise ValueError("El isbn ya existe")
        if self.vacia():
            self.insertar_inicio(libro)
            return
        actual = self.cabeza

        # recorre la lista hasta encontrar la posicion correcta
        # comparando alfabeticamente por titulo
        while actual and actual.libro.titulo.lower() < libro.titulo.lower():
            actual = actual.siguiente
        if actual == self.cabeza:
            self.insertar_inicio(libro)
        elif actual is None:
            self.insertar_final(libro)
        else:
            nuevo = nodoLibro(libro)
            anterior = actual.anterior
            anterior.siguiente = nuevo
            nuevo.anterior = anterior
            nuevo.siguiente = actual
            actual.anterior = nuevo
            self._cantidad += 1

    '''Consulta'''
    def buscar_isbn(self, isbn):
        '''buscara un libro por su isbn
        retornara si el libro se encuentra y None si no existe'''

        if not str(isbn).strip().isdigit():
            raise ValueError("isbn invalido")
        actual = self.cabeza
        while actual:
            if actual.libro.isbn == isbn:
                return actual.libro
            actual = actual.siguiente
        return None

    def buscar_autor(self, autor):
        '''busca libros por su autor exacto
        retorna si se encontro'''

        if not autor.strip():
            raise ValueError("autor invalido")
        resultados = []
        actual = self.cabeza
        while actual:
            if actual.libro.autor.lower() == autor.lower():
                resultados.append(actual.libro)
            actual = actual.siguiente
        return resultados

    def buscar_categoria(self, categoria):
        '''busca libro por su categoria exacta'''

        if not categoria.strip():
            raise ValueError("categoria invalida")
        resultados = []
        actual = self.cabeza
        while actual:
            if actual.libro.categoria.lower() == categoria.lower():
                resultados.append(actual.libro)
            actual = actual.siguiente
        return resultados
    
    '''actualiozar'''
    def actualizar_libro(self, isbn, titulo, autor, fecha, categoria):
        '''actualiza los datos de un libro existente
        retorna True si se actualizo y valueError si el sibn es invalido'''

        if not str(isbn).strip().isdigit():
            raise ValueError("isbn invalido")
        if not titulo.strip():
            raise ValueError("titulo invalido")
        if not autor.strip():
            raise ValueError("autor invalido")
        if not str(fecha).isdigit():
            raise ValueError("fecha invalida")
        if not categoria.strip():
            raise ValueError("categoria invalida")
        actual = self.cabeza
        while actual:
            if actual.libro.isbn == isbn:
                actual.libro.actualizar(titulo, autor, fecha, categoria)
                return True
            actual = actual.siguiente
        raise ValueError("Libro no encontrado")
    
    '''eliminar'''
    def eliminar_isbn(self, isbn):
        if not str(isbn).strip().isdigit():
            raise ValueError("isbn invalido")
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
        raise ValueError("Libro no encontrado")

    def __iter__(self):
        '''recorre la biblioteca como si fuera un for'''
        actual = self.cabeza
        while actual:
            yield actual.libro
            actual = actual.siguiente
