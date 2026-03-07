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
    
class MotorHotel:
    """
    Motor del sistema de reservas del hotel
    Usando dos pilas:
    -pila_reservas_actuales
    -pila_deshacer
    """

    def __init__(self):
        self.pila_reservas_actuales = []
        self.pila_deshacer = []

        self.contador_reservas = 1

    def reservar_habitacion(self, habitacion, fecha, cliente):
        """
        Se crea una nueva reserva si la habitacion esta disponible
        """

        if not habitacion.disponible:
            print("Error: La habitacion no esta disponible.")
            return
        
        reserva = Reserva(self.contador_reservas, habitacion, fecha, cliente)

        self.pila_reservas_actuales.append(reserva)

        habitacion.disponible = False

        self.contador_reservas += 1

        print("Reserva realizada correctamente")
        print(reserva)

    def cancelar_reserva(self):
        """
        Cancelar la ultima reserva(estructura tipo pila)
        """

        # verificar si hay reservas
        if not self.pila_reservas_actuales:
            print("No hay reservas para cancelar.")
            return
        
        # sacar la ultima reserva(LIFO)
        reserva = self.pila_reservas_actuales.pop()

        reserva.habitacion.disponible = True

        self.pila_deshacer.append(reserva)

        print("Reserva cancelada")
        print(reserva)

    def deshacer_cancelacion(self):
        """
        Recuepera la ultima reserva canceladad
        """
        # verifica si hay acciones para deshacer
        if not self.pila_deshacer:
            print("No hay accciones para deshacer.")
            return
        
        # recuperar la reserva cancelada
        reserva = self.pila_deshacer.pop()

        reserva.habitacion.disponible = False

        self.pila_reservas_actuales.append(reserva)

        print("Cancelacion deshecha:")
        print(reserva)

    def mostrar_reservas(self):
        """
        Muestra todas las reservas activas
        """

        print("\nReservas actuales:")

        # verificar si hay reservas
        if not self.pila_reservas_actuales:
            print("No hay reservas activas.")
            return
        
        # mostrar cada reserva
        for reserva in self.pila_reservas_actuales:
            print(reserva)

    def total_reservas(self):
        """
        Devuelve el numero total de reservas activas
        """

        return len(self.pila_reservas_actuales)