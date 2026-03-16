import sys
import os
import unittest

# agregar la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.gestion_datos import GestionHospital


class TestSistemaMedico(unittest.TestCase):

    def setUp(self):
        self.hospital = GestionHospital()

    # Prioridad de Emergencia
    def test_prioridad_emergencia(self):

        self.hospital.registrar_paciente("Juan", 2, "urgencias")
        self.hospital.registrar_paciente("Maria", 2, "urgencias")
        self.hospital.registrar_paciente("Pedro", 1, "urgencias")

        paciente = self.hospital.atender_paciente("urgencias")

        self.assertEqual(paciente.prioridad, 1)

    # Orden FIFO
    def test_fifo_regulares(self):

        self.hospital.registrar_paciente("A", 2, "urgencias")
        self.hospital.registrar_paciente("B", 2, "urgencias")
        self.hospital.registrar_paciente("C", 2, "urgencias")

        p1 = self.hospital.atender_paciente("urgencias")
        p2 = self.hospital.atender_paciente("urgencias")
        p3 = self.hospital.atender_paciente("urgencias")

        self.assertEqual(p1.nombre, "A")
        self.assertEqual(p2.nombre, "B")
        self.assertEqual(p3.nombre, "C")

    # Robustez cola vacía
    def test_cola_vacia(self):

        paciente = self.hospital.atender_paciente("urgencias")

        self.assertIsNone(paciente)

    # Estadística tiempo promedio
    def test_tiempo_promedio(self):

        self.hospital.registrar_paciente("Luis", 2, "urgencias")
        self.hospital.atender_paciente("urgencias")

        promedio = self.hospital.tiempo_promedio_espera()

        self.assertGreater(promedio, 0)


if __name__ == "__main__":
    unittest.main()