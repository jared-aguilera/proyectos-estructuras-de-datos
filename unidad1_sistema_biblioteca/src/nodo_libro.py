from __future__ import annotations
from typing import Optional
from libro import Libro   # Asumimos que la clase Libro esta definida en libro.py

class NodoLibro:
    """
    Nodo de una lista doblemente enlazada que contiene un objeto Libro.

    Atributos:
        dato (Libro): El libro almacenado en el nodo.
        siguiente (Optional[NodoLibro]): Referencia al siguiente nodo en la lista, o None si es el ultimo.
        anterior (Optional[NodoLibro]): Referencia al nodo anterior en la lista, o None si es el primero.
    """

    def __init__(self, libro: Libro) -> None:
        """
        Inicializa un nodo con el libro dado.

        Los enlaces 'siguiente' y 'anterior' se establecen inicialmente en None,
        ya que el nodo se crea sin conexiones.

        Args:
            libro: Objeto Libro que se almacenara en el nodo.
        """
        self.dato: Libro = libro
        self.siguiente: Optional[NodoLibro] = None
        self.anterior: Optional[NodoLibro] = None

    def __str__(self) -> str:
        """
        Representacion en cadena del nodo (delega en la representación del libro).

        Returns:
            str: El resultado de str(self.dato).
        """
        return str(self.dato)

    def __repr__(self) -> str:
        """
        Representacion oficial del nodo para depuracion.

        Returns:
            str: Una cadena que muestra el ISBN del libro contenido.
        """
        return f"NodoLibro(dato={self.dato.isbn})"