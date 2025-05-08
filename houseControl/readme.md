# Sistema de Control Inteligente

## Descripci�n

Este proyecto consiste en el desarrollo de un sistema integrado para
el control y monitoreo inteligente de dispositivos dom�sticos.
Utiliza la combinaci�n de una Raspberry Pi Pico y un ESP32 WROOM
(TTGO BOARD) para permitir la automatizaci�n basada en eventos y el
control remoto a trav�s de una interfaz de usuario accesible mediante
un bot de Telegram.

## Hardware

El sistema se basa en los siguientes componentes de hardware:

* **Raspberry Pi Pico:** Microcontrolador basado en el chip RP2040.
    Se encarga de gestionar solicitudes locales y controlar dispositivos.
* **M�dulo ESP8266:** Utilizado junto con la Raspberry Pi Pico para
    la conectividad a internet y el establecimiento de un servidor local.
* **ESP32 WROOM (TTGO BOARD):** M�dulo microcontrolador de doble
    n�cleo con capacidades avanzadas de conectividad (WiFi y Bluetooth).
    Gestiona el bot de Telegram y monitorea sensores.
* **Sensor de Movimiento RCWL-0516:** Sensor basado en radar Doppler
    para detectar la presencia de personas.
* **Sensor de Gas MQ5:** Sensor capaz de detectar gases combustibles.
* **Rel�s:** Utilizados para controlar el encendido y apagado de
    dispositivos como luces y la cafetera.

## Funcionalidades

El Sistema de Control Inteligente ofrece las siguientes funcionalidades:

* **Control Remoto a trav�s de Telegram:** Permite controlar
    dispositivos como la cafetera y las luces enviando comandos a un
    bot de Telegram.
    * Comandos disponibles: `cafe on`, `cafe off`, `luz on`, `luz off`,
        `buenas noches` (desactiva detecci�n de movimiento),
        `buenos dias` (activa detecci�n de movimiento),
        `encender pc` (Wake-on-LAN).
* **Iluminaci�n Automatizada por Movimiento:** Las luces pueden
    encenderse autom�ticamente al detectar movimiento mediante el sensor
    RCWL-0516.
* **Detecci�n y Alerta de Fugas de Gas:** El sensor MQ5 monitorea la
    concentraci�n de gas y env�a alertas instant�neas a trav�s del bot
    de Telegram si detecta una fuga.
* **Wake-on-LAN:** Permite encender una computadora de forma remota
    enviando un "magic packet".
* **Servidor Local en Raspberry Pi Pico:** La Pico, con el ESP8266,
    aloja un servidor HTTP para gestionar las solicitudes de control
    de dispositivos.
* **Comunicaci�n entre Microcontroladores:** El ESP32 interact�a
    con la Raspberry Pi Pico enviando solicitudes HTTP a los endpoints
    definidos en el servidor local de la Pico.

## M�dulo `esp8266_uart.py`

Este archivo contiene la clase `ESP8266ATWIFI`, encargada de gestionar
la comunicaci�n con el m�dulo ESP8266 desde la Raspberry Pi Pico a
trav�s de la interfaz UART. Utiliza comandos AT para:

* Conectar el ESP8266 a la red WiFi.
* Configurar y levantar un servidor HTTP en el ESP8266.
* Registrar y manejar los diferentes endpoints del servidor local.
* Enviar respuestas HTTP a los clientes.
* Generar y enviar el "magic packet" para la funci�n Wake-on-LAN.

Facilita la abstracci�n de la comunicaci�n serial con el m�dulo WiFi.

## Modo de Uso

Para utilizar el Sistema de Control Inteligente, se requiere configurar
ambos microcontroladores y conectarlos a una red WiFi estable.

1.  **Configuraci�n de Hardware:** Conectar la Raspberry Pi Pico con
    el m�dulo ESP8266 y los sensores y rel�s a los pines GPIO
    correspondientes en ambos microcontroladores.
2.  **Programaci�n de la Raspberry Pi Pico:** Cargar el c�digo
    MicroPython (`main.py`, `esp8266_uart.py`) para configurar el
    servidor local, manejar los endpoints y leer el sensor de
    movimiento. Es necesario un archivo de configuraci�n (`config.py`)
    con las credenciales WiFi y la direcci�n MAC para Wake-on-LAN.
3.  **Programaci�n del ESP32 WROOM:** Cargar el c�digo C++
    (`ESP32_hostBot.ino`) utilizando el Arduino IDE para configurar la
    conexi�n WiFi y con el bot de Telegram, manejar los comandos
    recibidos y leer el sensor de gas. Se requiere un archivo (`token.h`)
    con el token del bot de Telegram y los IDs de usuario autorizados.
4.  **Conexi�n a la Red WiFi:** Asegurarse de que ambos
    microcontroladores est�n conectados a la misma red WiFi.
5.  **Interacci�n con el Bot de Telegram:** Utilizar la aplicaci�n de
    Telegram para enviar los comandos predefinidos al bot y controlar
    los dispositivos o recibir alertas.

## Mejoras Deseadas

* Considerar el uso de protocolos de comunicaci�n m�s robustos o
    la implementaci�n de redundancias para asegurar una conexi�n
    estable entre los microcontroladores.
* Desarrollar una interfaz m�s avanzada en Telegram que permita
    una interacci�n m�s intuitiva y personalizada, incluyendo la
    visualizaci�n de estados en tiempo real.
* Implementar mecanismos para gestionar la autenticaci�n o
    autorizaci�n de usuarios que interact�an con el bot de Telegram.
* En el c�digo de la Raspberry Pi Pico, implementar el protocolo
    mDNS (Multicast DNS) para que la Pico pueda ser descubierta en
    la red por su nombre de host, evitando problemas si su direcci�n IP
    cambia tras un reinicio del m�dem o al usar uno diferente.
* Dise�ar el sistema de manera que permita la integraci�n de nuevos
    dispositivos y funcionalidades en el futuro.
