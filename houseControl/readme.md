# Sistema de Control Inteligente

## Descripción

Este proyecto consiste en el desarrollo de un sistema integrado para
el control y monitoreo inteligente de dispositivos domésticos.
Utiliza la combinación de una Raspberry Pi Pico y un ESP32 WROOM
(TTGO BOARD) para permitir la automatización basada en eventos y el
control remoto a través de una interfaz de usuario accesible mediante
un bot de Telegram.

## Hardware

El sistema se basa en los siguientes componentes de hardware:

* **Raspberry Pi Pico:** Microcontrolador basado en el chip RP2040.
    Se encarga de gestionar solicitudes locales y controlar dispositivos.
* **Módulo ESP8266:** Utilizado junto con la Raspberry Pi Pico para
    la conectividad a internet y el establecimiento de un servidor local.
* **ESP32 WROOM (TTGO BOARD):** Módulo microcontrolador de doble
    núcleo con capacidades avanzadas de conectividad (WiFi y Bluetooth).
    Gestiona el bot de Telegram y monitorea sensores.
* **Sensor de Movimiento RCWL-0516:** Sensor basado en radar Doppler
    para detectar la presencia de personas.
* **Sensor de Gas MQ5:** Sensor capaz de detectar gases combustibles.
* **Relés:** Utilizados para controlar el encendido y apagado de
    dispositivos como luces y la cafetera.

## Funcionalidades

El Sistema de Control Inteligente ofrece las siguientes funcionalidades:

* **Control Remoto a través de Telegram:** Permite controlar
    dispositivos como la cafetera y las luces enviando comandos a un
    bot de Telegram.
    * Comandos disponibles: `cafe on`, `cafe off`, `luz on`, `luz off`,
        `buenas noches` (desactiva detección de movimiento),
        `buenos dias` (activa detección de movimiento),
        `encender pc` (Wake-on-LAN).
* **Iluminación Automatizada por Movimiento:** Las luces pueden
    encenderse automáticamente al detectar movimiento mediante el sensor
    RCWL-0516.
* **Detección y Alerta de Fugas de Gas:** El sensor MQ5 monitorea la
    concentración de gas y envía alertas instantáneas a través del bot
    de Telegram si detecta una fuga.
* **Wake-on-LAN:** Permite encender una computadora de forma remota
    enviando un "magic packet".
* **Servidor Local en Raspberry Pi Pico:** La Pico, con el ESP8266,
    aloja un servidor HTTP para gestionar las solicitudes de control
    de dispositivos.
* **Comunicación entre Microcontroladores:** El ESP32 interactúa
    con la Raspberry Pi Pico enviando solicitudes HTTP a los endpoints
    definidos en el servidor local de la Pico.

## Módulo `esp8266_uart.py`

Este archivo contiene la clase `ESP8266ATWIFI`, encargada de gestionar
la comunicación con el módulo ESP8266 desde la Raspberry Pi Pico a
través de la interfaz UART. Utiliza comandos AT para:

* Conectar el ESP8266 a la red WiFi.
* Configurar y levantar un servidor HTTP en el ESP8266.
* Registrar y manejar los diferentes endpoints del servidor local.
* Enviar respuestas HTTP a los clientes.
* Generar y enviar el "magic packet" para la función Wake-on-LAN.

Facilita la abstracción de la comunicación serial con el módulo WiFi.

## Modo de Uso

Para utilizar el Sistema de Control Inteligente, se requiere configurar
ambos microcontroladores y conectarlos a una red WiFi estable.

1.  **Configuración de Hardware:** Conectar la Raspberry Pi Pico con
    el módulo ESP8266 y los sensores y relés a los pines GPIO
    correspondientes en ambos microcontroladores.
2.  **Programación de la Raspberry Pi Pico:** Cargar el código
    MicroPython (`main.py`, `esp8266_uart.py`) para configurar el
    servidor local, manejar los endpoints y leer el sensor de
    movimiento. Es necesario un archivo de configuración (`config.py`)
    con las credenciales WiFi y la dirección MAC para Wake-on-LAN.
3.  **Programación del ESP32 WROOM:** Cargar el código C++
    (`ESP32_hostBot.ino`) utilizando el Arduino IDE para configurar la
    conexión WiFi y con el bot de Telegram, manejar los comandos
    recibidos y leer el sensor de gas. Se requiere un archivo (`token.h`)
    con el token del bot de Telegram y los IDs de usuario autorizados.
4.  **Conexión a la Red WiFi:** Asegurarse de que ambos
    microcontroladores estén conectados a la misma red WiFi.
5.  **Interacción con el Bot de Telegram:** Utilizar la aplicación de
    Telegram para enviar los comandos predefinidos al bot y controlar
    los dispositivos o recibir alertas.

## Mejoras Deseadas

* Considerar el uso de protocolos de comunicación más robustos o
    la implementación de redundancias para asegurar una conexión
    estable entre los microcontroladores.
* Desarrollar una interfaz más avanzada en Telegram que permita
    una interacción más intuitiva y personalizada, incluyendo la
    visualización de estados en tiempo real.
* Implementar mecanismos para gestionar la autenticación o
    autorización de usuarios que interactúan con el bot de Telegram.
* En el código de la Raspberry Pi Pico, implementar el protocolo
    mDNS (Multicast DNS) para que la Pico pueda ser descubierta en
    la red por su nombre de host, evitando problemas si su dirección IP
    cambia tras un reinicio del módem o al usar uno diferente.
* Diseñar el sistema de manera que permita la integración de nuevos
    dispositivos y funcionalidades en el futuro.
