# Sistema de Gestión de Atención Médica - Unidad 3 (Colas)

## Descripción
Este proyecto consiste en un sistema profesional para la gestión de flujos de pacientes en un entorno hospitalario desarrollado en Python. El núcleo del sistema utiliza una **Estructura de Datos de Cola de Prioridad** implementada con `deques` para garantizar que las emergencias médicas reciban atención inmediata mientras se respeta el orden de llegada para los casos regulares.

## Características Principales
* **Cola de Prioridad Dual**: Implementación de una estructura que gestiona dos colas internas (emergencias y regulares) para priorizar turnos de forma automatizada.
* **Gestión Multi-Departamento**: Control independiente de filas de espera para los departamentos de Urgencias, Pediatría y Medicina General.
* **Sistema de Reservas Proactivo**: Permite programar citas para horarios futuros con un verificador automático que activa al paciente en la sala de espera al llegar la hora pactada.
* **Persistencia de Datos**: Almacenamiento y carga automática de pacientes, historial y reservas mediante archivos JSON localizados en la carpeta `data`.
* **Estadísticas y Reportes**: Cálculo en tiempo real de tiempos de espera promedio y generación de un reporte físico en formato `.txt` con el desglose de eficiencia por área.
* **Interfaz Gráfica (GUI)**: Entorno visual moderno desarrollado con la librería `customtkinter`, utilizando un sistema de tarjetas dinámicas con códigos de colores.
* **Notificaciones de Turno**: Sistema de alertas visuales mediante cuadros de mensaje para avisar al personal y pacientes cuando es momento de pasar a consulta.

## Tecnologías Utilizadas
* **Lenguaje**: Python 3.13
* **Interfaz**: CustomTkinter
* **Persistencia**: Formato JSON
* **Pruebas**: Framework Unittest

## Estructura del Proyecto
De acuerdo con la organización actual en el repositorio:

unidad3_sistema_medico/
|-- data/
|   |-- pacientes.json
|   |-- reporte_eficiencia.txt
|-- diagramas/
|   |-- diagrama_secuencia.png
|   |-- diagrama_uml.png
|-- docs/
|   |-- reporte_practica.pdf
|   |-- manual_usuario.pdf
|-- src/
|   |-- app_medica.py
|   |-- gestion_datos.py
|   |-- modelos.py
|   |-- motor_medico.py
|-- tests/
|   |-- test_sistema_medico.py
|-- README.md

## Instrucciones de Ejecucion
1. Instalar las dependencias necesarias:
   pip install customtkinter tkcalendar

2. Ejecutar el sistema desde la terminal:
   python unidad3_sistema_medico/src/app_medica.py

3. Para ejecutar las pruebas unitarias:
   python unidad3_sistema_medico/tests/test_sistema_medico.py

## Equipo de Desarrollo (Equipo 2)
* David Osvaldo Calderon Salgado
* Absalon Castellano Flores
* Miguel Angel Lara Tarin
* Jared Alejandro Lopez Aguilera

Docente: Jose Manuel Muñoz Contreras
UABC - Facultad de Ciencias de la Ingenieria y Tecnologia