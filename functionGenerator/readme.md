# Generador de Funciones a partir de Salida de Audio

## Descripción

Este proyecto desarrolla un generador de funciones utilizando la
salida de audio de un dispositivo electrónico (como un celular o
computadora) y una etapa de protección y amplificación basada en un
amplificador operacional. Permite generar señales con diferentes formas
de onda y frecuencias a bajo costo, aprovechando herramientas de
uso cotidiano. Se utilizará una aplicación móvil para generar las
funciones desde el dispositivo de audio.

## Justificación

Este proyecto surge de la necesidad de demostrar las habilidades
adquiridas en el laboratorio de electrónica, tanto en investigación
como en trabajo práctico. Se buscó crear un generador de funciones
accesible, utilizando la salida de audio de dispositivos comunes y
componentes de bajo costo que se tenían a disposición, como el
amplificador operacional LM358. El uso de una fuente de alimentación
de 5V, fácilmente obtenible de cargadores de celular, también responde
a la idea de utilizar recursos cotidianos. El diseño se centró en el
ancho de banda audible (hasta 22 kHz), coherente con la fuente de
señal de audio empleada.

## Hardware

Los componentes principales del proyecto son:

* **Amplificador Operacional LM358:** Utilizado para la etapa de
    protección y amplificación de la señal de audio.
* **Dispositivo con Salida de Audio:** Un celular, computadora u otro
    dispositivo capaz de ejecutar la aplicación generadora de funciones
    y emitir audio.
* **Componentes Pasivos:** Resistencias y capacitores necesarios para
    configurar el circuito amplificador y las etapas de protección.
    (Ver lista completa en la sección de componentes del reporte).
* **Fuente de Alimentación:** Una fuente de 5V para alimentar el
    circuito (por ejemplo, un cargador de celular).

## Funcionalidades

El generador de funciones permite:

* Generar **formas de onda** sinusoidal, cuadrada y triangular.
* Controlar la **frecuencia**, **amplitud** y **fase** de la señal generada
    (mediante la aplicación).
* Amplificar la señal de audio para obtener un mayor voltaje de
    salida.
* Proteger la salida de audio del dispositivo generador de posibles
    daños causados por el circuito amplificador.
* Operar con una única fuente de alimentación positiva (5V).

## Modo de Uso

Para utilizar el generador de funciones, sigue los pasos:

1.  **Instala la aplicación:** Descarga e instala la aplicación **Function**
    **Generator**
    ([https://play.google.com/store/apps/details?id=com.keuwl.functiongenerator](https://play.google.com/store/apps/details?id=com.keuwl.functiongenerator))
    en tu dispositivo móvil o tablet.
2.  **Ensambla el circuito:** Arma el circuito del amplificador operacional
    según el diseño propuesto en la documentación del proyecto.
    Asegúrate de utilizar los valores de componentes adecuados.
3.  **Conecta la alimentación:** Alimenta el circuito con una fuente de 5V.
4.  **Conecta la salida de audio:** Conecta la salida de audio de tu
    dispositivo (donde instalaste la app) a la entrada del circuito
    amplificador.
5.  **Genera la señal:** Abre la aplicación Function Generator y configura
    la forma de onda, frecuencia y amplitud deseadas. Activa la salida
    de audio desde la aplicación.
6.  **Obtén la señal de salida:** La señal generada, amplificada y
    protegida estará disponible a la salida del circuito con amplificador
    operacional.
