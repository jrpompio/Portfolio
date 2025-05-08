# Juego Golpea al Topo

## Descripción

Este proyecto implementa el clásico juego "Golpea al Topo"
utilizando Python y la biblioteca GTK para la interfaz gráfica.
Incluye un menú de configuración para ajustar parámetros del juego
y registra los mejores puntajes obtenidos.

## Requisitos

Para ejecutar este juego, necesitas tener instalado:

* Python 3
* PyGObject (para GTK 3)
* Pygame (para la reproducción de sonidos)

Puedes instalar las dependencias usando pip:
`pip install PyGObject pygame`

## Funcionalidades

* **Menú de Configuración:** Permite ajustar el número de agujeros,
    la cantidad de intentos y la velocidad de aparición del topo.
* **Interfaz Gráfica del Juego:** Muestra los agujeros donde puede
    aparecer el topo.
* **Aparición Aleatoria:** El topo aparece aleatoriamente en uno
    de los agujeros.
* **Cálculo de Puntaje:** Mide el tiempo de reacción al golpear
    el topo y calcula el promedio.
* **Registro de Mejores Puntajes:** Guarda y muestra los 10
    mejores promedios de tiempo.
* **Sonidos:** Reproduce sonidos al golpear un topo o fallar.

## Modo de Uso

1.  Asegúrate de tener Python y las bibliotecas necesarias instaladas.
2.  Abre una terminal o línea de comandos.
3.  **Estando en el directorio de este programa, ejecuta:**
    `python3 proyecto.py`
