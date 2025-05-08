
from machine import Pin
import esp8266_uart as wifi
import config  # Importa las configuraciones del archivo config.py
import _thread
import time

# Configuración de pines para sensor y relé
sensor_pin = Pin(18, Pin.IN)
rele = Pin(25, Pin.OUT)

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
)

# Instancia de WiFiManager con depuración activada y mensaje personalizado
wifi_manager = wifi.ESP8266ATWIFI(ssid, password, uart_num, tx_pin, rx_pin, baudrate,
                                  I_WANT_TO_DEPURATE_THIS_FS=False,
                                  default_not_found_message=not_found_message)

# Variables de control
movement_detected = False
last_movement_time = 0

# Funciones específicas para cada endpoint


def handle_wol_request():
    wifi_manager.connect()
    wifi_manager.send_magic_packet(mac_address)
    wifi_manager.start_server()


def handle_light_on():
    global movement_detected, last_movement_time
    movement_detected = True
    last_movement_time = time.time()
    rele.value(1)


def handle_light_off():
    """Apaga el LED y cancela cualquier extensión de tiempo."""
    global movement_detected
    print("[handle_light_off] Apagando luz manualmente.")
    movement_detected = False  # Cancela la detección de movimiento
    rele.value(0)


# Función para monitorear el sensor y controlar el LED
def pin_monitor():
    global movement_detected, last_movement_time

    while True:
        sensor_state = sensor_pin.value()
        current_time = time.time()  # Obtén el tiempo actual en segundos

        if sensor_state == 1:  # Movimiento detectado
            movement_detected = True
            last_movement_time = current_time  # Actualiza el tiempo del último movimiento
            rele.value(1)  # Enciende el LED
        else:
            # Verifica si ha pasado una hora sin movimiento
            if movement_detected and current_time - last_movement_time >= 3:  # 3600 segundos = 1 hora
                movement_detected = False  # Restablece el estado
                rele.value(0)  # Apaga el LED
                api_url = "http://www.timeapi.io/api/Time/current/zone?timeZone=America/Costa_Rica"
                a, b = wifi_manager.get_hour_and_minutes(api_url)
                print(a)
                print(b)

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


# Escucha de solicitudes
wifi_manager.listen()
