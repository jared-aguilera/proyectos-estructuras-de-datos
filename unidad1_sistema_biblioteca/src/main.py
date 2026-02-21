from sistema_gestion import SistemaGestion


def main() -> None:
    """Punto de entrada del sistema"""
    app = SistemaGestion()
    app.ejecutar()


if __name__ == "__main__":
    main()