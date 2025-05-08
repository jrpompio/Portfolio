import time
import binascii
from machine import UART, Pin


class ESP8266ATWIFI:
    def __init__(self, ssid, password, uart_num, tx_pin, rx_pin, baudrate=115200,
                 I_WANT_TO_DEPURATE_THIS_FS=True, default_not_found_message="Endpoint no encontrado."):
        """
        Inicializa el WiFiManager con los datos de conexión WiFi y la configuración de UART.

        Args:
            ssid (str): Nombre de la red WiFi.
            password (str): Contraseña de la red WiFi.
            uart_num (int): Número del UART (por ejemplo, 0 o 1).
            tx_pin (int): Número del pin para UART TX.
            rx_pin (int): Número del pin para UART RX.
            baudrate (int): Velocidad de la comunicación UART.
            I_WANT_TO_DEPURATE_THIS_FS (bool): Si es True, imprime mensajes de depuración.
            default_not_found_message (str): Mensaje predeterminado para rutas no encontradas.
        """
        self.ssid = ssid
        self.password = password
        self.uart = UART(uart_num, baudrate=baudrate,
                         tx=Pin(tx_pin), rx=Pin(rx_pin))
        self.endpoints = {}  # Diccionario para almacenar los endpoints
        self.I_WANT_TO_DEPURATE_THIS_FS = I_WANT_TO_DEPURATE_THIS_FS
        self.default_not_found_message = default_not_found_message

    def debug_print(self, message):
        """Imprime mensajes de depuración si está habilitado."""
        if self.I_WANT_TO_DEPURATE_THIS_FS:
            print(message)

    def await_response(self, timeout=5):
        """Espera una respuesta desde el módulo UART dentro de un tiempo límite."""
        self.debug_print(
            f"[await_response] Iniciando espera por respuesta con timeout={timeout}s")
        start_time = time.time()
        while time.time() - start_time < timeout:
            response = self.uart.read()
            if response:
                self.debug_print(
                    f"[await_response] Respuesta recibida: {response}")
                return response
        self.debug_print("[await_response] Timeout alcanzado, sin respuesta")
        return None

    def send_command(self, cmd, timeout=5):
        """Envía un comando al módulo UART y espera una respuesta."""
        self.debug_print(
            f"[send_command] Enviando comando: {cmd}, con timeout={timeout}s")
        self.uart.write(cmd + '\r\n')
        response = self.await_response(timeout)
        if response:
            try:
                decoded_response = response.decode()
                self.debug_print(
                    f"[send_command] Respuesta decodificada: {decoded_response}")
            except UnicodeError:
                self.debug_print(
                    "[send_command] Error al decodificar la respuesta. Mostrando en crudo:")
                self.debug_print(' '.join(f'{byte:02X}' for byte in response))
        else:
            self.debug_print(
                f"[send_command] Sin respuesta al comando '{cmd}'")
        return response

    def connect(self, max_retries=3):
        """Conecta el ESP8266 a una red WiFi."""
        self.debug_print("[WiFiManager] Reiniciando el módulo WiFi...")
        self.send_command('AT+RST', 2)
        time.sleep(2)  # Pausa para permitir reinicio
        self.uart.read()  # Limpia el buffer

        self.debug_print("[WiFiManager] Configurando modo cliente...")
        self.send_command('AT+CWMODE=1', 2)

        for attempt in range(max_retries):
            self.debug_print(
                f"[WiFiManager] Intento de conexión al WiFi ({attempt + 1}/{max_retries})...")
            response = self.send_command(
                f'AT+CWJAP="{self.ssid}","{self.password}"', 15)
            time.sleep(10)  # Pausa tras el intento de conexión

            if response and (b"WIFI CONNECTED" in response or b"WIFI GOT IP" in response):
                self.debug_print("[WiFiManager] Conexión exitosa.")
                break
            else:
                self.debug_print(
                    "[WiFiManager] Error al conectar, reintentando...")
        else:
            self.debug_print(
                "[WiFiManager] Error: No se pudo conectar al WiFi tras varios intentos.")

        self.debug_print("[WiFiManager] Obteniendo información de red...")
        self.send_command('AT+CIFSR', 10)
        time.sleep(1)

    def start_server(self, port=80):
        """Configura e inicia un servidor HTTP."""
        self.debug_print("[WiFiManager] Iniciando servidor HTTP...")
        self.send_command('AT+CIPMUX=1', 2)
        self.send_command(f'AT+CIPSERVER=1,{port}', 2)

    def add_endpoint(self, endpoint, handler, response_message):
        """Registra un endpoint con su función de manejo y mensaje de respuesta."""
        self.debug_print(f"[WiFiManager] Registrando endpoint: {endpoint}")
        self.endpoints[endpoint] = (handler, response_message)

    def listen(self):
        """Escucha solicitudes HTTP y ejecuta el manejador correspondiente."""
        self.debug_print("[WiFiManager] Escuchando solicitudes HTTP...")
        while True:
            response = self.await_response(10)
            if response and b"+IPD" in response:
                try:
                    request_str = response.decode('utf-8')
                except UnicodeDecodeError:
                    request_str = ""

                self.debug_print("[WiFiManager] Solicitud recibida:")
                self.debug_print(request_str)

                for endpoint, (handler, response_message) in self.endpoints.items():
                    if f"GET {endpoint}" in request_str:
                        self.send_http_response(response_message)
                        self.send_command('AT+CIPCLOSE=0')
                        handler()  # Ejecuta la función asociada
                        break
                else:
                    self.send_http_response(self.default_not_found_message)

    def send_http_response(self, message):
        """Envía una respuesta HTTP básica."""
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: {}\r\n\r\n"
            "{}"
        ).format(len(message), message)
        self.send_command('AT+CIPSEND=0,{}'.format(len(response)), 2)
        self.uart.write(response)
        time.sleep(1)

    def send_magic_packet(self, mac_address):
        """Genera y envía un Magic Packet para Wake-on-LAN."""
        mac_bytes = binascii.unhexlify(
            mac_address.replace(":", "").replace("-", ""))
        if len(mac_bytes) != 6:
            raise ValueError("La dirección MAC debe tener 6 bytes.")

        magic_packet = b'\xFF' * 6 + mac_bytes * 16
        broadcast_ip = "255.255.255.255"
        port = 9

        self.send_command(f'AT+CIPSTART="UDP","{broadcast_ip}",{port}', 2)
        self.send_command(f'AT+CIPSEND={len(magic_packet)}')
        self.uart.write(magic_packet)
        time.sleep(1)
        self.send_command('AT+CIPCLOSE')

    # no sirve, probablemente por el listener
    # def get_hour_and_minutes(self, api_url):
    #     """
    #     Obtiene y muestra la hora y los minutos desde la respuesta HTTP.

    #     Args:
    #         api_url (str): URL completa del API.

    #     Returns:
    #         None: Imprime la hora y los minutos extraídos de la línea 'Date:'.
    #     """
    #     self.debug_print(f"Conectando al servidor: {api_url}")

    #     # Intentar cerrar conexiones previas
    #     self.send_command('AT+CIPCLOSE', 2)

    #     # Parsear el host y el endpoint desde el URL
    #     try:
    #         host = api_url.split("/")[2]
    #         endpoint = "/" + "/".join(api_url.split("/")[3:])
    #     except IndexError:
    #         self.debug_print("[get_hour_and_minutes] URL invalido")
    #         return None, None

    #     # Iniciar conexión TCP
    #     response = self.send_command(f'AT+CIPSTART="TCP","{host}",80', 5)
    #     if b"ERROR" in response:
    #         self.debug_print("Error al conectar al servidor.")
    #         return None, None

    #     # Pausa para estabilizar la conexión
    #     time.sleep(0.5)

    #     # Crear el mensaje HTTP GET
    #     http_request = "GET {} HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n".format(
    #         endpoint, host)

    #     # Enviar la solicitud HTTP
    #     self.send_command(f'AT+CIPSEND={len(http_request)}', 2)
    #     self.uart.write(http_request)

    #     # Leer respuesta en fragmentos
    #     raw_response = b""
    #     while True:
    #         chunk = self.await_response(5)
    #         if not chunk:
    #             break
    #         raw_response += chunk

    #     # Intentar decodificar la respuesta
    #     try:
    #         decoded_response = raw_response.decode("utf-8")
    #         self.debug_print("\nRespuesta decodificada:")
    #         self.debug_print(decoded_response)

    #         # Buscar la línea con "Date:"
    #         for line in decoded_response.split("\r\n"):
    #             if line.startswith("Date:"):
    #                 # Extraer la fecha y hora
    #                 date_time = line.split("Date: ")[1]
    #                 self.debug_print(f"\nFecha y hora obtenidas: {date_time}")

    #                 # Extraer la hora y minutos
    #                 # HH:MM:SS está en la 4 posición
    #                 time_part = date_time.split(" ")[4]
    #                 hour, minutes, _ = time_part.split(":")
    #                 self.debug_print(f"Hora actual: {hour}:{minutes}")
    #                 return hour, minutes
    #         self.debug_print(
    #             "\n[Error] No se encontró la línea con 'Date:' en la respuesta.")
    #     except Exception:
    #         self.debug_print("\n[Error] No se pudo decodificar la respuesta.")
    #         return None, None