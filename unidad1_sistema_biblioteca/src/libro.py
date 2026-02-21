class Libro:
    """Representa un libro de la biblioteca."""

    def __init__(self, titulo: str, autor: str, anio: int, isbn: str, categoria: str):
        self.titulo = titulo
        self.autor = autor
        self.anio = anio
        self.isbn = isbn
        self.categoria = categoria

    def actualizar(self, titulo: str, autor: str, anio: int, categoria: str) -> None:
        """Actualiza los datos del libro (excepto ISBN)."""
        self.titulo = titulo
        self.autor = autor
        self.anio = anio
        self.categoria = categoria

    def __str__(self) -> str:
        return f"[{self.isbn}] {self.titulo} - {self.autor} ({self.anio}) [{self.categoria}]"
