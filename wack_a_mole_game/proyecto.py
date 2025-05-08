#!/usr/bin/python3

# Nombre y carné del estudiante que realiza el código:
# Junior Ruiz Sánchez - B97026
# Este programa se basa en el juego de "golpea al topo"
# para ello se usa gtk mostrando un menú el cual tiene parámetros
# que modifican el juego, así como la cantidad de agujeros,
# cantidad de repeticiones, y tiempo de salida del topo.
# Después también usando gtk muestra agujeros y mediante un random
# se cambia la imagen del agujero por una del topo en el agujero
# y al darle clic se calcula la diferencia de tiempo entre cuando
# la imagen fue cambiada hasta cuando se dio clic, además se ejecuta
# un sonido y a su vez muestra y guarda
# el promedio de las diferencias de tiempo.

# importando librerías necesarias
# Para corregir error de representación en punto flotante Decimal
from decimal import Decimal
import random  # Para números aleatorios
import time  # para la diferencia de tiempo
from pygame import mixer  # Para reproducción de sonidos
import gi  # para la interfaz gráfica
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib # noqa

# Se crea una clase para ejecutar el código
# de mejor manera y reusar código


class WhackAMole:
    def __init__(self, file):
        # valores para objeto gtk
        self.builder = Gtk.Builder()
        self.builder.add_from_file(file)
        # comportamiento de los handlers
        self.handlers = {
            "onDestroy": Gtk.main_quit,
            "onButtonClicked": self.on_button_clicked,
        }
        self.builder.connect_signals(self.handlers)
        # se definen las variables a usar en el constructor
        self.grid = 16  # tamaño de agujeros por defecto
        self.times = 3  # repeticiones por defecto
        # velocidad de salida del topo por defecto
        self.mole_speed = 0.5
        self.start_time = 0  # tiempo inicial
        # fragmento de tiempo al salir del topo
        self.fragment_time_start = 0
        self.counter = 0  # contador para detener intentos
        self.score = []  # declaración de lista para puntaje
        # declaración de lista para mostrar puntajes
        self.print_scores = " "

    # definiendo método para iniciar juego
    def start_game(self):
        # definiendo parámetros de objeto gtk para juego
        window = self.builder.get_object("lvl{}".format(self.grid))
        # cambio de título de ventana
        window.set_title('Golpea al topo de {} casillas'.format(
            self.grid))
        window.set_default_size(800, 800)
        # cambiando todas las casillas por imagen de agujero
        for i in range(1, self.grid + 1):
            self.change_button_image("cell_{}_{}".format(
                self.grid, i), "image/hole.png"
            )
        # mostrando interfaz del juego
        window.show_all()
        # uso de GLib para ejecutar una acción de gtk en determinado
        # tiempo, acá es donde se define el tiempo de salida del topo
        GLib.timeout_add(1000 * self.mole_speed, self.random_mole,
                         self.grid)

    # Se define método para cambiar imagen de un botón
    def change_button_image(self, button_id, image_path):
        button = self.builder.get_object(button_id)
        image = Gtk.Image.new_from_file(image_path)
        button.set_image(image)

    # Se define método para salida aleatoria del topo
    def random_mole(self, cells):
        mole_cell = random.randint(1, cells)
        # usando el método change_button_image y el posible string
        # ya que todos los botones de se llaman
        # cell_(número de agujeros)_(número de celda)
        self.change_button_image("cell_{}_{}".format(
                                 self.grid, mole_cell),
                                 "image/mole.png"
                                 )

        # se obtiene el tiempo actual
        # para obtener la marca del tiempo de salida del topo
        self.fragment_time_start = time.time()

    # se define método para manejar botones
    def on_button_clicked(self, button):
        # se obtiene el id del botón
        name = Gtk.Buildable.get_name(button)
        # caso para el botón de inicio del juego (en el menú)
        if name == "startgame":
            self.score = []
            self.counter = 0
            self.get_parameters()
            self.builder.get_object("menu").hide()
            self.start_game()
        # caso para mostrar los puntajes (en el menú)
        elif name == "score":
            self.get_score()
            self.show_dialog(self.print_scores)
        # caso para cerrar el programa (en el menú)
        elif name == "exit":
            Gtk.main_quit()
            # todos los demás casos que son los botones
            # correspondientes a los agujeros o topos
        else:
            # se obtiene el objeto de imagen del botón
            image = button.get_image()
            # se obtiene el valor de ruta de imagen del botón
            image_name = image.get_property("file")
            # en caso de que la imagen del botón sea un topo
            if image_name == "image/mole.png":
                # se obtiene el tiempo actual
                # para obtener la marca de tiempo
                # de cuando se golpea al topo
                fragment_time_end = time.time()
                # dicho botón se cambia a un agujero
                # de esta forma se perciba haber golpeado al topo
                self.change_button_image(name, "image/hole.png")
                # para poder obtener la diferencia
                # entre el tiempo de inicio (cuando sale el topo)
                # y el tiempo del clic (cuando se golpea al topo)
                diff = fragment_time_end - self.fragment_time_start
                # se agrega esta diferencia a la lista score
                self.score.append(diff)
                # se reproduce el sonido de golpe
                mixer.music.load('sounds/hit.mp3')
                mixer.music.play()
                # if para repetir las oportunidades de golpe
                # hasta que el contador llegue a un valor definido
                # por el usuario (self.times)
                if self.counter < self.times - 1:
                    # aumento del contador
                    self.turn_counter()
                    # se vuelve a lanzar el mismo juego
                    self.start_game()
                # else para cuando el contador llegue a su fin
                else:
                    # se calcula el promedio
                    promedio = round(
                        # uso de Decimal para evitar
                        # error de punto flotante
                        Decimal(
                            sum(self.score) / len(self.score)
                        ),
                        5) * 1000

                    # se multiplica por 1000 para obtener
                    # el valor en milisegundos
                    # Se muestra este promedio
                    self.show_dialog("El promedio es: {} "
                                     "milisegundos".format(
                                                promedio))
                    # se guarda este promedio
                    # en el "scores/scores.txt"
                    self.save_score(promedio)
                    # se oculta la ventana game
                    self.builder.get_object("lvl{}".format(
                        self.grid)).hide()
                    self.start_menu()
            # Para el caso de que la imagen del botón
            # sea un agujero
            elif image_name == "image/hole.png":
                # se reproduce una risa molesta
                mixer.music.load('sounds/mole_laugh.mp3')
                mixer.music.play()

    # Se define contador para detener los turnos de golpe al topo
    def turn_counter(self):
        self.counter += 1

    # Se define método para mostrar ventana de dialogo
    @staticmethod
    def show_dialog(message):
        dialog = Gtk.MessageDialog(
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.run()
        dialog.destroy()

    # Se define metodo para iniciar el menú
    def start_menu(self):
        menu = self.builder.get_object("menu")
        menu.set_title("Menu")  # cambio de título de ventana
        menu.show_all()

    # Se define método para obtención de parámetros
    # de lanzamiento del juego
    def get_parameters(self):
        # Obtención del parámetro de turnos para golpear al topo
        spin_button = self.builder.get_object('times')
        spin_value = spin_button.get_value()
        # Obtención del parámetro de tiempo de salida del topo
        scale_button = self.builder.get_object('time_up')
        scale_value = scale_button.get_value()
        # Obtención del parámetro de agujeros
        radio_button1 = self.builder.get_object('rcells_1')
        radio_button2 = self.builder.get_object('rcells_2')
        radio_button3 = self.builder.get_object('rcells_3')
        if radio_button1.get_active():
            radio_value = 4
        elif radio_button2.get_active():
            radio_value = 9
        elif radio_button3.get_active():
            radio_value = 16
        else:
            radio_value = 4
        # cambio de los parámetros por defecto
        # a los parámetros seleccionados
        self.grid = radio_value
        self.times = spin_value
        self.mole_speed = scale_value

    # Se define método para guardar un valor en documento de texto
    @staticmethod
    def save_score(score_add):
        file_txt = "scores/scores.txt"  # se define ruta de archivo
        current_results = []  # se define lista de resultados actuales
        # lectura del archivo
        try:
            with open(file_txt, "r") as file:
                for line in file:
                    current_results.append(float(line))
        except FileNotFoundError:
            pass
        # adición del valor a la lista
        score_add = float(score_add)
        current_results.append(score_add)
        # se ordena de menor a mayor
        current_results.sort()
        # se obtienen solo los primeros 10 valores
        current_results = current_results[:10]
        # Se escribe la lista en el documento de texto
        with open(file_txt, "w") as file:
            for score_add in current_results:
                file.write(str(score_add) + "\n")

    # Se define un método para presentar la
    # información del archivo de texto correspondiente a los puntajes
    def get_score(self):
        # Se define la ruta del archivo
        file_txt = "scores/scores.txt"
        current_results = []  # Se declara la lista
        # Se hace lectura del archivo
        try:
            with open(file_txt, "r") as file:
                for line in file:
                    current_results.append(float(line))
        except FileNotFoundError:
            pass
        # Definición de la cadena de caracteres mediante un for
        scores_print = "Mejores puntajes :\n"
        for i, score in enumerate(current_results, start=1):
            scores_print += "# {} : {} milisegundos\n".format(i,
                                                              score)
            # Se redefine el valor de print_scores
        self.print_scores = scores_print


# Cuerpo de código
if __name__ == "__main__":
    # Se obtienen los valores del .glade y se convierten a objeto
    gtk_object = WhackAMole("proyecto.glade")
    # Se usa el método de inicio de menú
    gtk_object.start_menu()
    # Se inicializa el método mixer de pygame para reproducir sonido
    mixer.init()
    # Se reproduce el sonido de inicio de menú
    mixer.music.load('sounds/start.mp3')
    mixer.music.play()
    # Se inicia método de Gtk para mantener las ventanas abiertas
    # y el código en ejecución
    Gtk.main()
