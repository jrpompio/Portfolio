from machine import Pin
import esp8266_uart as wifi
import config  # Importa las configuraciones del archivo config.py
import _thread
import time

# Configuración de pines para sensor y relé
sensor_pin = Pin(18, Pin.IN)
rele = Pin(19, Pin.OUT)
led = Pin(25, Pin.OUT)
rele.value(0)
led.value(0)

# Configuración WiFi y UART
ssid = config.SSID
password = config.PASSWORD
mac_address = config.MAC_ADDRESS
uart_num = 0  # UART 0
tx_pin = 0
rx_pin = 1
baudrate = 115200

not_found_message = (
    "Endpoints disponibles:\n"
    "/wol: Para encender la computadora\n"
    "/luzon: para encender la luz\n"
    "/luzoff: para apagar la luz\n"
    "/goodn: para desactivar la deteccion\n"
    "/goodm: para activar la deteccion\n"
)

# Instancia de WiFiManager con depuración activada y mensaje personalizado
wifi_manager = wifi.ESP8266ATWIFI(ssid, password, uart_num, tx_pin, rx_pin, baudrate,
                                  I_WANT_TO_DEPURATE_THIS_FS=True,
                                  default_not_found_message=not_found_message)

# Variables de control
movement_detected = False
last_movement_time = 0
motion_handler = True
# Funciones específicas para cada endpoint


def handle_wol_request():
    wifi_manager.connect()
    wifi_manager.send_magic_packet(mac_address)
    wifi_manager.start_server()


def handle_light_on():
    global movement_detected, last_movement_time, motion_handler
    movement_detected = True
    motion_handler = True
    last_movement_time = time.time()
    rele.value(1)
    led.value(1)


def handle_light_off():
    """Apaga el LED y cancela cualquier extensión de tiempo."""
    global movement_detected, motion_handler
    movement_detected = False  # Cancela la detección de movimiento
    motion_handler = False
    rele.value(0)
    led.value(0)


def handle_good_night():
    global motion_handler
    motion_handler = False


def handle_good_morning():
    global motion_handler
    motion_handler = True

# Función para monitorear el sensor y controlar el LED


def pin_monitor():
    global movement_detected, last_movement_time, motion_handler

    while True:
        sensor_state = sensor_pin.value()
        current_time = time.time()  # Obtén el tiempo actual en segundos

        if sensor_state == 1 and motion_handler:
            movement_detected = True
            last_movement_time = current_time  # Actualiza el tiempo del último movimiento
            rele.value(1)  # Enciende el LED
            led.value(1)  # Enciende el LED
        else:
            # Verifica si ha pasado una hora sin movimiento
            if movement_detected and current_time - last_movement_time >= 4:  # 3600 segundos = 1 hora
                movement_detected = False  # Restablece el estado
                rele.value(0)  # Apaga el LED
                led.value(0)  # Apaga el LED

        time.sleep(0.1)  # Pausa breve para evitar saturar el procesador


# Inicia el hilo para monitorear el sensor
_thread.start_new_thread(pin_monitor, ())

# Configuración de la red y el servidor HTTP
wifi_manager.connect()
wifi_manager.start_server()

# Registro de endpoints
wifi_manager.add_endpoint("/wol", handle_wol_request,
                          "Encendiendo computadora.\n")
wifi_manager.add_endpoint("/luzon", handle_light_on, "Luz encendida.\n")
wifi_manager.add_endpoint("/luzoff", handle_light_off, "Luz apagada.\n")
wifi_manager.add_endpoint("/goodn", handle_good_night,
                          "Deteccion desactivada.\n")
wifi_manager.add_endpoint("/goodm", handle_good_morning,
                          "Deteccion activada.\n")


# Escucha de solicitudes
wifi_manager.listen()
