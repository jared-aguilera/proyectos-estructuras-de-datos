class Libro:
    """Representa un libro de la biblioteca."""

    def __init__(self, titulo: str, autor: str, año: int, isbn: str, categoria: str):
        self.titulo = titulo
        self.autor = autor
        self.anio = año
        self.isbn = isbn
        self.categoria = categoria

    def actualizar(self, titulo: str, autor: str, año: int, categoria: str) -> None:
        """Actualiza los datos del libro (excepto ISBN)."""
        self.titulo = titulo
        self.autor = autor
        self.anio = año
        self.categoria = categoria

    def __str__(self) -> str:
        return f"[{self.isbn}] {self.titulo} - {self.autor} ({self.año}) [{self.categoria}]"