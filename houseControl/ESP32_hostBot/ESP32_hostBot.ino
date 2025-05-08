#include "CTBot.h"
#include "token.h"
#include <WiFi.h>
#include <HTTPClient.h>

CTBot miBot;
TBMessage msg;

// Definir pines
const int relePin = 4;  // Cambia este pin según sea necesario
const int sensorPin = 34; // Pin analógico conectado al sensor

// Umbral para activar el LED (1V en una escala de 0 a 3.3V)
const float voltageThreshold = 1.0; 
const int adcMax = 4095;             // Resolución ADC del ESP32 (12 bits)
const float referenceVoltage = 3.3; // Voltaje de referencia

// Variables para temporizador con millis
unsigned long startTime = 0;          // Tiempo de inicio del temporizador
unsigned long timeGas = 0;            // Tiempo de inicio de fuga de gas
const unsigned long interval = 20000; // 30 minutos en milisegundos (30 * 60 * 1000)
bool cafeteraEncendida = false;       // Estado de la cafetera

void setup() {
  Serial.begin(115200);
  Serial.println("Inicializando...");
  
  miBot.wifiConnect(ssid, password);
  miBot.setTelegramToken(token);

  if (miBot.testConnection()) {
    Serial.println("Conexion exitosa. UwU");
  } else {
    Serial.println("Conexion fallida. UnU");
  }

  pinMode(sensorPin, INPUT);
  pinMode(relePin, OUTPUT);   // Configuración del pin GPIO como salida
  digitalWrite(relePin, LOW); // Asegurarse de que el relé está apagado inicialmente
}

void loop() {
  // Verificar si la cafetera está encendida y si el temporizador ha expirado
  if (cafeteraEncendida && (millis() - startTime >= interval)) {
    apagarCafetera();
    miBot.sendMessage(msg.sender.id, "Han pasado 30 minutos. Cafetera apagada.");
  }

  // Manejar mensajes de Telegram
  if (CTBotMessageText == miBot.getNewMessage(msg)) {
    manejarComando();
  }

  detectorGas();

  delay(250); // Reducir la carga de la CPU
}

void manejarComando() {
  if (msg.text.equalsIgnoreCase("cafe on")) {
    if (!cafeteraEncendida) {
      encenderCafetera();
      miBot.sendMessage(msg.sender.id, "Cafetera encendida. (por 30 minutos)");
    } 
    else {
      miBot.sendMessage(msg.sender.id, "La cafetera ya está encendida.");
    }
  } 
  else if (msg.text.equalsIgnoreCase("cafe off")) {
    if (cafeteraEncendida) {
      apagarCafetera();
      miBot.sendMessage(msg.sender.id, "Cafetera apagada.");
    } else {
      miBot.sendMessage(msg.sender.id, "La cafetera ya está apagada.");
    }
  } 
  else if (msg.text.equalsIgnoreCase("buenas noches")) {
    //realizarSolicitudHTTP("http://192.168.0.10/goodn");
    //realizarSolicitudHTTP("http://192.168.0.11/goodn");
    realizarSolicitudHTTP("http://192.168.17.195/goodn");
    miBot.sendMessage(msg.sender.id, "Buenas noches");
  } else if (msg.text.equalsIgnoreCase("buenos dias")) {
    //realizarSolicitudHTTP("http://192.168.0.10/goodm");
    //realizarSolicitudHTTP("http://192.168.0.11/goodm");
    realizarSolicitudHTTP("http://192.168.17.195/goodm");
    miBot.sendMessage(msg.sender.id, "Buenos dias");
  } else if (msg.text.equalsIgnoreCase("luz on")) {
    //realizarSolicitudHTTP("http://192.168.0.10/luzon");
    //realizarSolicitudHTTP("http://192.168.0.11/luzon");
    realizarSolicitudHTTP("http://192.168.17.195/luzon");
    miBot.sendMessage(msg.sender.id, "Se envió la solicitud para encender la luz.");
  } else if (msg.text.equalsIgnoreCase("luz off")) {
    //realizarSolicitudHTTP("http://192.168.0.10/luzoff");
    //realizarSolicitudHTTP("http://192.168.0.11/luzoff");
    realizarSolicitudHTTP("http://192.168.17.195/luzoff");
    miBot.sendMessage(msg.sender.id, "Se envió la solicitud para apagar la luz.");
  } else if (msg.text.equalsIgnoreCase("encender pc")) {
    //realizarSolicitudHTTP("http://192.168.0.10/wol");
    //realizarSolicitudHTTP("http://192.168.0.11/wol");
    realizarSolicitudHTTP("http://192.168.17.195/wol");
    miBot.sendMessage(msg.sender.id, "Se envió la solicitud para encender la computadora.");
  } else {
    String reply = (String)"Hola " + msg.sender.username + ". Intenta escribir encender pc, cafe on, cafe off, luz on o luz off, buenos dias o buenas noches.";
    miBot.sendMessage(msg.sender.id, reply);
  }
}

void encenderCafetera() {
  digitalWrite(relePin, HIGH);  // Encender el relé
  startTime = millis();         // Registrar el tiempo de inicio
  cafeteraEncendida = true;     // Actualizar el estado
  Serial.println("Cafetera encendida. Temporizador iniciado.");
  Serial.println(msg.sender.id);
}

void apagarCafetera() {
  digitalWrite(relePin, LOW);  // Apagar el relé
  cafeteraEncendida = false;  // Actualizar el estado
  Serial.println("Cafetera apagada.");
}

void realizarSolicitudHTTP(const String& url) {
  HTTPClient http;
  WiFiClient client;

  Serial.println("Realizando solicitud HTTP a: " + url);
  http.begin(client, url);   // Iniciar conexión HTTP
  http.GET();                // Realizar la solicitud GET
  http.end();                // Finalizar conexión
}

void detectorGas() {
    int sensorValue = analogRead(sensorPin);
  // Convertir la lectura del ADC a voltaje
  float sensorVoltage = (sensorValue * referenceVoltage) / adcMax;

  // Comparar el voltaje con el umbral
  if (sensorVoltage > voltageThreshold/2 && sensorVoltage < voltageThreshold) {
    if (millis() - timeGas >= interval) {
      miBot.sendMessage(user1, "Importante: Podrías tener una fuga de gas."); 
      miBot.sendMessage(user2, "Importante: Podrías tener una fuga de gas.");
      timeGas = millis(); 
    } 
  } else if (sensorVoltage > voltageThreshold) {
    miBot.sendMessage(user1, "URGENTE: TIENES UNA FUGA DE GAS!");
    miBot.sendMessage(user2, "URGENTE: TIENES UNA FUGA DE GAS!");
    delay(30000);
  }
}
