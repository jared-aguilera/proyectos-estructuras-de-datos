import sys
import os
import unittest
import time

# Configuración del entorno: se agrega la carpeta 'src' al path del sistema.
# Esto permite que el test importe 'gestion_datos' y que este encuentre
# correctamente a 'motor_medico' y 'modelos' sin usar rutas relativas.
ruta_src = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.append(ruta_src)

from gestion_datos import GestionHospital


class TestSistemaMedico(unittest.TestCase):
    """
    Pruebas unitarias para validar la lógica de colas, prioridades,
    validaciones de datos y sistema de reservas del hospital.
    """

    def setUp(self):
        """
        Configuración inicial antes de cada prueba.
        Inicializa una instancia limpia del hospital y vacía las colas.
        """
        self.hospital = GestionHospital()
        # Limpiar el historial y colas para asegurar independencia entre tests
        self.hospital.historial = []
        self.hospital.reservas = []
        for cola in self.hospital.departamentos.values():
            cola.emergencias.clear()
            cola.regulares.clear()

    def test_prioridad_emergencia(self):
        """
        Verifica que las emergencias (P1) tengan precedencia sobre
        los casos regulares (P2) independientemente del orden de llegada.
        """
        self.hospital.registrar_paciente("Juan", 2, "urgencias")
        self.hospital.registrar_paciente("Maria", 2, "urgencias")
        self.hospital.registrar_paciente("Pedro", 1, "urgencias")

        paciente = self.hospital.atender_paciente("urgencias")
        # Debe ser Pedro por ser prioridad 1
        self.assertEqual(paciente.nombre, "Pedro")
        self.assertEqual(paciente.prioridad, 1)

    def test_fifo_regulares(self):
        """
        Verifica que pacientes con la misma prioridad se atiendan
        siguiendo estrictamente el orden de llegada (FIFO).
        """
        self.hospital.registrar_paciente("Paciente A", 2, "urgencias")
        self.hospital.registrar_paciente("Paciente B", 2, "urgencias")

        p1 = self.hospital.atender_paciente("urgencias")
        p2 = self.hospital.atender_paciente("urgencias")

        self.assertEqual(p1.nombre, "Paciente A")
        self.assertEqual(p2.nombre, "Paciente B")

    def test_validacion_nombres(self):
        """
        Prueba que el sistema rechace correctamente nombres que
        contengan números o que se encuentren vacíos.
        """
        # Prueba con caracteres no permitidos
        exito_num, _ = self.hospital.registrar_paciente("Jared123", 2, "urgencias")
        # Prueba con campo vacío
        exito_vacio, _ = self.hospital.registrar_paciente("", 2, "urgencias")

        self.assertFalse(exito_num)
        self.assertFalse(exito_vacio)

    def test_reserva_futura(self):
        """
        Valida que se pueda agendar una cita correctamente para
        un horario posterior al actual de forma dinámica.
        """
        # Obtenemos la hora actual en formato de texto
        hora_actual = time.strftime('%H:%M')
        
        # Intentamos generar una hora 2 minutos en el futuro
        hora_futura = time.strftime('%H:%M', time.localtime(time.time() + 120))
        
        if hora_futura < hora_actual:
            hora_futura = "23:59"
        
        exito, mensaje = self.hospital.registrar_reserva("Miguel", "urgencias", hora_futura)
        
        # Ahora la aserción siempre debería ser True
        self.assertTrue(exito)
        self.assertIn("Cita agendada", mensaje)

    def test_reserva_pasada_rechazada(self):
        """
        Valida que el sistema bloquee el registro de citas en
        horarios que ya han transcurrido.
        """
        # Intento de agendar a las 00:01 am
        exito, _ = self.hospital.registrar_reserva("David", "pediatria", "00:01")
        self.assertFalse(exito)

    def test_cola_vacia(self):
        """
        Verifica que intentar atender en un departamento sin pacientes
        no provoque errores y devuelva None.
        """
        paciente = self.hospital.atender_paciente("medicina_general")
        self.assertIsNone(paciente)

    def test_estadisticas_promedio(self):
        """
        Verifica que el cálculo del tiempo promedio de espera se
        realice correctamente tras atender a un paciente.
        """
        self.hospital.registrar_paciente("Absalon", 2, "urgencias")
        # Pequeña pausa para generar un diferencial de tiempo
        time.sleep(0.1)
        self.hospital.atender_paciente("urgencias")

        promedio = self.hospital.tiempo_promedio_espera()
        self.assertGreater(promedio, 0)


if __name__ == "__main__":
    unittest.main()