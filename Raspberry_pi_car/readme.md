**Nota:** Los archivos de código de este proyecto no se incluyen aquí
por ser propiedad del tcu.

# Control de Carrito Robótico

## Descripción

Este proyecto consiste en el desarrollo del software para controlar
un carrito robótico avanzado. El objetivo principal fue implementar
la lógica de control y la interfaz necesaria para operar el carrito
de manera local y remota, utilizando diferentes periféricos de
entrada. Se trabajó en entender el hardware existente para poder
programar eficientemente sus funcionalidades.

## Hardware

El hardware del carrito robótico, aunque no fue diseñado ni construido
como parte de este proyecto de software, se compone de los
siguientes elementos clave que fueron integrados mediante programación:

* **Raspberry Pi 3 Model B:** Microcomputadora principal del carrito.
* **Puente H:** Permite controlar la dirección y velocidad de los
    motores DC.
* **Controlador de Servos:** Gestiona el movimiento de múltiples
    servomotores.
* **4 Motores DC:** Responsables de la tracción y movimiento general
    del carrito.
* **6 Servomotores:** Utilizados para movimientos de precisión
    (manipuladores, sensores, etc.).
* **Pantalla Táctil:** Interfaz de usuario local para interactuar
    directamente con el carrito.

## Directorios y Archivos Clave

El código del proyecto está organizado en diferentes directorios y
archivos.

* El directorio `control/` contiene los scripts principales para la
    operación del carrito:
    * `TropicalBot.py`: Comunicación con el controlador de servos
        (`adafruit_pca9685`).
    * `bot_handler.py`: Instrucciones para motores DC y servomotores.
    * `config_handler.py`: Maneja la configuración personalizada de
        cada carrito.
    * `mando.py`: Control mediante mando de Xbox.
    * `teclado.py`: Control mediante teclado.

* Los scripts de prueba y desarrollo se encuentran en el directorio
    `desarrollo/`.

* El archivo `menu.py`, que implementa la interfaz táctil, se
    encuentra en el directorio raíz del proyecto, al mismo nivel que
    `control/` y `desarrollo/`.

## Principio de Diseño

El software fue desarrollado aplicando el **Principio de Responsabilidad**
**Única**. Cada módulo o archivo se diseñó para tener una única
responsabilidad bien definida, lo que facilita la organización del código,
su mantenimiento y la escalabilidad del proyecto.

## Herramientas para Desarrolladores

Se crearon scripts y herramientas específicas para asistir en el
desarrollo, prueba y depuración del software y el hardware del carrito.
Estas herramientas incluyen funcionalidades para:

* Probar individualmente un servomotor conectado.
* Probar el funcionamiento de los motores DC.
* Determinar el tiempo óptimo para el movimiento suave de los
    servomotores.
* Realizar pruebas de la entrada de control desde el mando de Xbox.
* Verificar la entrada de control desde el teclado.
* Apagar de forma segura todos los servomotores.
* Ejecutar una prueba remota simultánea en varios carritos.

## Menú Táctil

Se implementó un menú interactivo adaptado a la pantalla táctil de
los carritos. Este menú permite a los usuarios interactuar con el
sistema sin necesidad de usar la terminal, ofreciendo opciones para:

* Ejecutar secuencias de movimientos predefinidas (figuras).
* Iniciar los servicios de control remoto (ya sea por mando o teclado).
* Detener cualquier acción o servicio en ejecución en el carrito.
