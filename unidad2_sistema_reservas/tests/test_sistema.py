import unittest
import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from motor_hotel import SistemaReservasHotel
from pila import PilaPersonalizada

class TestSistemaReservasHotel(unittest.TestCase):
    """
    Conjunto de pruebas unitarias para el sistema de reservas.
    """

    def setUp(self):
        """
        Configuración inicial para cada prueba.
        """
        self.hotel = SistemaReservasHotel()

    def test_inicializacion_sistema(self):
        """
        Prueba la inicialización correcta del sistema.
        """
        self.assertEqual(self.hotel.contador_reservas, 1)
        self.assertEqual(len(self.hotel.habitaciones), 6)
        self.assertTrue(self.hotel.pila_reservas_actuales.is_empty())
        self.assertTrue(self.hotel.pila_deshacer.is_empty())

    def test_reserva_exitosa(self):
        """
        Prueba una reserva exitosa.
        """
        resultado = self.hotel.reservar_habitacion("Test Cliente", "2025-12-25", "Simple")
        self.assertTrue(resultado)
        self.assertEqual(self.hotel.pila_reservas_actuales.size(), 1)
        self.assertEqual(self.hotel.contador_reservas, 2)

    def test_fecha_invalida(self):
        """
        Prueba el manejo de fechas inválidas.
        """
        resultado = self.hotel.reservar_habitacion("Test Cliente", "fecha-invalida", "Simple")
        self.assertFalse(resultado)
        self.assertEqual(self.hotel.pila_reservas_actuales.size(), 0)

    def test_habitaciones_agotadas(self):
        """
        Prueba el comportamiento cuando no hay habitaciones disponibles.
        """
        clientes = [f"Cliente{i}" for i in range(1, 8)]

        for i, cliente in enumerate(clientes[:6], 1):
            fecha = f"2025-12-{i+24:02d}"
            self.hotel.reservar_habitacion(cliente, fecha)

        resultado = self.hotel.reservar_habitacion("Cliente Extra", "2025-12-31")
        self.assertFalse(resultado)

    def test_cancelacion_exitosa(self):
        """
        Prueba la cancelación exitosa de una reserva.
        """
        self.hotel.reservar_habitacion("Test Cliente", "2025-12-25")
        reserva_id = 1

        resultado = self.hotel.cancelar_reserva(reserva_id)
        self.assertTrue(resultado)

        self.assertEqual(self.hotel.pila_reservas_actuales.size(), 0)
        self.assertEqual(self.hotel.pila_deshacer.size(), 1)

    def test_cancelacion_reserva_inexistente(self):
        """
        Prueba cancelar una reserva que no existe.
        """
        resultado = self.hotel.cancelar_reserva(999)
        self.assertFalse(resultado)

    def test_deshacer_cancelacion(self):
        """
        Prueba deshacer una cancelación.
        """
        self.hotel.reservar_habitacion("Test Cliente", "2025-12-25")
        self.hotel.cancelar_reserva(1)

        resultado = self.hotel.deshacer_cancelacion()
        self.assertTrue(resultado)
        self.assertEqual(self.hotel.pila_reservas_actuales.size(), 1)
        self.assertEqual(self.hotel.pila_deshacer.size(), 0)

    def test_deshacer_sin_cancelaciones(self):
        """
        Prueba deshacer cuando no hay cancelaciones.
        """
        resultado = self.hotel.deshacer_cancelacion()
        self.assertFalse(resultado)


class TestPilaPersonalizada(unittest.TestCase):
    """
    Pruebas unitarias específicas para la clase PilaPersonalizada.
    """

    def setUp(self):
        """
        Configuración inicial para cada prueba.
        """
        self.pila = PilaPersonalizada(3)

    def test_pila_vacia_inicial(self):
        """
        Prueba que la pila esté inicialmente vacía.
        """
        self.assertTrue(self.pila.is_empty())
        self.assertFalse(self.pila.is_full())
        self.assertEqual(self.pila.size(), 0)

    def test_push_y_pop(self):
        """
        Prueba operaciones básicas push y pop.
        """
        elemento = "test"
        self.pila.push(elemento)

        self.assertFalse(self.pila.is_empty())
        self.assertEqual(self.pila.size(), 1)

        resultado = self.pila.pop()
        self.assertEqual(resultado, elemento)
        self.assertTrue(self.pila.is_empty())

    def test_peek_sin_modificar(self):
        """
        Prueba que peek no modifique la pila.
        """
        elemento = "test"
        self.pila.push(elemento)

        resultado = self.pila.peek()
        self.assertEqual(resultado, elemento)
        self.assertEqual(self.pila.size(), 1)

    def test_overflow_error(self):
        """
        Prueba que se lance OverflowError al exceder capacidad.
        """
        for i in range(3):
            self.pila.push(f"elemento{i}")

        self.assertTrue(self.pila.is_full())

        with self.assertRaises(OverflowError):
            self.pila.push("overflow")

    def test_underflow_error(self):
        """
        Prueba que se lance IndexError al hacer pop en pila vacía.
        """
        with self.assertRaises(IndexError):
            self.pila.pop()

        with self.assertRaises(IndexError):
            self.pila.peek()

    def test_orden_lifo(self):
        """
        Prueba que la pila mantenga el orden LIFO.
        """
        elementos = ["primero", "segundo", "tercero"]

        for elem in elementos:
            self.pila.push(elem)

        for elem in reversed(elementos):
            self.assertEqual(self.pila.pop(), elem)


def ejecutar_pruebas():
    """
    Ejecuta todas las pruebas unitarias.
    """
    print("Ejecutando pruebas unitarias...")
    print("="*50)

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSistemaReservasHotel))
    suite.addTest(unittest.makeSuite(TestPilaPersonalizada))

    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)

    print(f"\nPruebas ejecutadas: {resultado.testsRun}")
    print(f"Fallas: {len(resultado.failures)}")
    print(f"Errores: {len(resultado.errors)}")

    if resultado.wasSuccessful():
        print("Todas las pruebas pasaron exitosamente!")
    else:
        print("Algunas pruebas fallaron.")

