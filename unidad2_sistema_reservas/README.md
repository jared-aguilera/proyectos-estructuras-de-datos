# Sistema de Reservacion de Hotel - Unidad 2 (Pilas)

## Descripcion
Este proyecto consiste en un sistema integral para la gestion de reservaciones hoteleras desarrollado en Python para la materia de Estructuras de Datos. El nucleo del sistema utiliza una Estructura de Datos de Pila (Stack) implementada desde cero para gestionar el historial de reservaciones y permitir la funcionalidad de deshacer cancelaciones.

## Caracteristicas Principales
* Pila LIFO Personalizada: Implementacion propia de una estructura de datos tipo pila con todos los metodos requeridos (push, pop, peek, is_empty, is_full).
* Funcion de Deshacer (Undo): Uso de una pila secundaria (pila_deshacer) para restaurar la ultima reservacion cancelada de forma instantanea.
* Persistencia de Datos: Guardado y carga automatica de informacion mediante archivos JSON localizados en la carpeta data.
* Interfaz Grafica (GUI): Entorno visual moderno desarrollado con la libreria customtkinter.
* Busqueda Multi-criterio: Filtros dinamicos para localizar reservas por nombre de cliente, numero de habitacion o fecha.
* Gestion de Estancias: Calculo automatico del costo total de la reserva basado en el numero de noches y el tipo de habitacion.
* Validaciones y Robustez: Restricciones de fecha para evitar registros pasados y manejo de excepciones para evitar errores de desbordamiento de pila.

## Tecnologias Utilizadas
* Lenguaje: Python 3.13
* Interfaz: CustomTkinter y tkcalendar
* Persistencia: Formato JSON
* Pruebas: Framework Unittest

## Estructura del Proyecto
De acuerdo con la organizacion actual en el repositorio:

unidad2_sistema_reservas/
|-- data/
|   |-- reservas.json
|-- diagramas/
|   |-- diagrama_secuencia.png
|   |-- diagrama_uml.png
|-- docs/
|   |-- informe_tecnico.pdf
|-- src/
|   |-- main_gui.py
|   |-- modelos.py
|   |-- motor_hotel.py
|   |-- pila.py
|-- tests/
|   |-- test_sistema.py
|-- README.md

## Instrucciones de Ejecucion
1. Instalar las dependencias necesarias:
   pip install customtkinter tkcalendar

2. Ejecutar el sistema desde la terminal:
   python unidad2_sistema_reservas/src/main_gui.py

3. Para ejecutar las pruebas unitarias:
   python unidad2_sistema_reservas/tests/test_sistema.py

## Equipo de Desarrollo (Equipo 2)
* David Osvaldo Calderon Salgado
* Absalon Castellano Flores
* Miguel Angel Lara Tarin
* Jared Alejandro Lopez Aguilera

Docente: Jose Manuel Muñoz Contreras
UABC - Facultad de Ciencias de la Ingenieria y Tecnologia