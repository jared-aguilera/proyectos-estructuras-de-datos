class Habitacion:
    """
    Clase para manejar los datos de cada cuarto del hotel
    """
    def __init__(self, numero, tipo, precio):
        self.numero = numero
        self.tipo = tipo
        self.precio = precio
        self.disponible = True

    def __str__(self):
        # Usamos un if sencillo para poner si esta libre o no
        estado = "Libre" if self.disponible else "No disponible"
        return f"Habitacion {self.numero} | {self.tipo} - Precio : ${self.precio} - {estado}"
    def __repr__(self):
        return self.__str__()
    
class Reserva:
    """
    Gestiona la vinculacion entre un cliente, una habitacion y una fecha especifica
    """
    def __init__(self, id_reserva, habitacion, fecha, cliente, noches=1):
        self.id_reserva = id_reserva
        self.habitacion = habitacion
        self.fecha = fecha
        self.cliente = cliente
        self.noches = noches
        # Calculamos el costo total multiplicando el precio de la habitación por las noches
        self.costo_total = self.habitacion.precio * self.noches

    def __str__(self):
        return (f"Reserva #{self.id_reserva}: {self.cliente} | "
                f"Hab: {self.habitacion.numero} ({self.habitacion.tipo}) | "
                f"Entrada: {self.fecha} | Noches: {self.noches} | "
                f"Total: ${self.costo_total}")
    
    def __repr__(self):
        return self.__str__()