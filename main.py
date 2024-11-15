import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
import json

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0) 

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Window Title')

# Parámetros partida
noms_jugadors = ['taronja','lila','blau']
fichas_iniciales = [(100,0),(50,1),(20,1),(10,2),(5,2)] # Las tuplas son: (NomFicha, Cantidad)
resultats = []

# Bucle de l'aplicació
def main():
    is_looping = True

    # Inicia jugadores
    init_jugadors()

    while is_looping:
        is_looping = app_events()
        app_run()
        app_draw()

        clock.tick(60) # Limitar a 60 FPS

    # Fora del bucle, tancar l'aplicació
    pygame.quit()
    sys.exit()

# Gestionar events
def app_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Botó tancar finestra
            return False
        # Posición del mouse
        # Click pulsado
        # Click soltado
    return True

# Fer càlculs
def app_run():
    pass

    # Reorganizamos fichas de jugadores, 'per tal que, amb el crèdit disponible, hi hagi la màxima varietat de valors de fitxe possible.'

    # IF estamos en 'Modo Ruleta'

        # Si hay dinero apostado y se aprieta botón de apostar, hace apuesta
        # Se añade la información de la tirada al array 'resultats': Para cada jugador --> (resultado numérico de la apuesta, crédito después de tirada, cuánto ha apostado jugador)

    # ELIF estamos en 'Modo Estadísticas'

        # Modifica valor de scroll si se está moviendo

    # Comprueba si partida ha acabado

# Dibuixar
def app_draw():
    # Pintar el fons de blanc
    screen.fill(WHITE)

    # Dibuja ruleta o estadísticas
    '''Dependiendo del valor de una variable, en la misma zona de la pantalla se muestra la ruleta o un listado de estadísticas.'''

    # Dibuja sección jugadores

    # Dibuja sección banca

    # Dibuja secciones apuestas

    # Dibuja Fichas
    '''Fichas estáticas en pantalla + Fichas en movimiento (si las hay)'''

    # Actualitzar el dibuix a la finestra
    pygame.display.update()

def init_jugadors():
    '''Inicia el diccionario que contiene información de los jugadores.'''
    global jugadors
    jugadors = {}
    for nom_jugador in noms_jugadors:
        dict_jugador = {}
        for ficha in fichas_iniciales:
            nom_ficha = f'{ficha[0]:03}'
            valor_ficha = ficha[1]
            dict_jugador[nom_ficha] = valor_ficha
        jugadors[nom_jugador] = dict_jugador
    

if __name__ == "__main__":
    main()