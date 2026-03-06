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
    def __init__(self, id_reserva, habitacion, fecha, cliente):
        self.id_reserva = id_reserva
        self.habitacion = habitacion
        self.fecha = fecha
        self.cliente = cliente

    def __str__(self):
        # Aqui sacamos el numero directamente desde el objeto habitacion
        return f"Reserva #{self.id_reserva}: Por el cliente {self.cliente} en la habitacion {self.habitacion.numero} el dia {self.fecha}"
    def __repr__(self):
        return self.__str__()