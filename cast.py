"""
(0 a 30 puntos) [Criterio subjetivo] Según la estética de su nivel

(0 a 30 puntos) Según cuantos fps pueda renderizar su software

(10 puntos) Por colocar un contador de fps
    -10 pts

(20 puntos) Por implementar una cámara con movimiento hacia delante y hacia atrás y rotación (como la que hicimos en clase)
    -20 pts
(10 puntos) Por implementar rotación con el mouse (solo horizontal)
    -10 pts

(10 puntos) Por implementar un minimapa que muestre la posición de jugador en el mundo. No puede estar lado a lado del mapa principal, debe estar en una esquina. 
    -10 pts

(5 puntos) Por agregar música de fondo.
    -5 pts
(10 puntos) Por agregar efectos de sonido
    -10 pts

(5 puntos) Por agregar una pantalla de bienvenida 
    -5 pts
(10 puntos mas) si la pantalla permite seleccionar entre multiples niveles 
    -10 pts
(10 puntos) Por agregar una pantalla de exito cuando se cumpla una condicion en el nivel
    -10 pts

TOTAL (sin criterios subjetivos): 90 pts
TOTAL (con criterios subjetivos): 150 pts (30pts de estética y 30pts de FPS)
"""

import pygame
from math import *
import pygame_menu
from pygame import mixer
from Raycaster import *
from pygame.locals import *

BLACK = (0,0,0)
WHITE = (255,255,255)
SKY = (21,49,70)
GROUND = (172,58,65)
TRANSPARENT = (152,0,136,255)

myimage = pygame_menu.baseimage.BaseImage(
    image_path = './imagenes/rosalia.jpg',
    drawing_mode = pygame_menu.baseimage.IMAGE_MODE_FILL,
)

nextLevel = pygame.image.load('./imagenes/success.png')
failed = pygame.image.load('./imagenes/failed.png')

######################################################### THEME MENU PRINCIPAL
Theme = pygame_menu.themes.Theme
Rosalia_Theme = Theme(background_color = myimage, title_background_color = (116, 0, 1),title_font = pygame_menu.font.FONT_FRANCHISE,title_font_size = 100,cursor_selection_color = (255, 255, 255),widget_font = pygame_menu.font.FONT_FRANCHISE,widget_alignment = pygame_menu.locals.ALIGN_CENTER,widget_font_color=(0, 0, 0),widget_background_color=(116, 0, 1),widget_padding = (10,20),widget_margin = (0,20)) 
pygame.init()
screen = pygame.display.set_mode((600,500))

def FPS():
    fps = str("FPS: "+str(int((pygame.time.Clock()).get_fps())))
    return (pygame.font.SysFont("Arial", 20)).render(fps, 10, pygame.Color("white"))

def music(music):
    """MUSICA DE FONDO"""
    mixer.music.stop()
    mixer.music.load(music)
    mixer.music.play(-1)
    mixer.music.set_volume(0.1)
    """MUSICA DE FONDO"""

def soundeffect(music):
    """EFFECTS"""
    effect = mixer.Sound(music)
    effect.set_volume(0.2)
    effect.play()
    """EFFECTS"""

def running(screen, map, musica):
    r = Raycaster(screen)
    r.load_map(map)

    ultima_x = r.player['x']
    ultima_y = r.player['y']

    counter, text = 60, '60'.rjust(3)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('Arial', 15)
    text = ""

    music(musica)
    soundeffect('./soundeffects/Coin_Mario_01.mp3')     

    sound = True
    running = True
    clock = pygame.time.Clock()

    while running:
        if(r.player['x'] >= 370 and r.player['y'] >= 405):
            r.completed = True


        if counter <= 0:
            if sound:
                soundeffect('./soundeffects/Coin_Mario_01.mp3')  
                sound = False

            screen.fill(BLACK,(0,0,600,r.height))
            for x in range(0,600):
                for y in range(0,500):
                    c = failed.get_at((x,y))
                    r.point(x,y,c)
            
            pygame.display.update()

            pygame.event.clear()
            while True:
                event = pygame.event.wait()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        soundeffect('./soundeffects/Coin_Mario_01.mp3')  
                        sound = False
                        running = False
                        break        

        elif r.completed:
            if sound:
                soundeffect('./soundeffects/Coin_Mario_01.mp3')  
                sound = False

            screen.fill(BLACK,(0,0,600,r.height))
            for x in range(0,600):
                for y in range(0,496):
                    c = nextLevel.get_at((x,y))
                    r.point(x,y,c)
            
            pygame.display.update()

            pygame.event.clear()
            while True:
                event = pygame.event.wait()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        soundeffect('./soundeffects/Coin_Mario_01.mp3')  
                        sound = False
                        running = False
                        break    

        else:
            screen.fill(BLACK,(0,0,100,r.height))
            screen.fill(SKY,(100,0,900,r.height/2))
            screen.fill(GROUND, (100,r.height/2,900,r.height/2))

            try:
                r.render()
                r.clearZ()
            except:
                r.player['x'] = ultima_x
                r.player['y'] = ultima_y

            ultima_x = r.player['x']
            ultima_y = r.player['y']

            for event in pygame.event.get():

                if event.type == pygame.USEREVENT: 
                    counter -= 1
                    text = str(counter).rjust(3) if counter > 0 else 'boom!'

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        r.player['a'] -= pi/10
                    if event.key == pygame.K_d:
                        r.player['a'] += pi/10

                    #movement with keys (up, down, left, right)
                    if event.key == pygame.K_UP:
                        r.player['x'] += cos(r.player['a']) * 10
                        r.player['y'] += sin(r.player['a']) * 10
                    if event.key == pygame.K_DOWN:
                        r.player['x'] -= cos(r.player['a']) * 10
                        r.player['y'] -= sin(r.player['a']) * 10
                    if event.key == pygame.K_LEFT:
                        r.player['x'] -= cos(r.player['a'] + pi/2) * 10
                        r.player['y'] -= sin(r.player['a'] + pi/2) * 10
                    if event.key == pygame.K_RIGHT:
                        r.player['x'] += cos(r.player['a'] + pi/2) * 10
                        r.player['y'] += sin(r.player['a'] + pi/2) * 10

                #rotation with mouse
                if event.type == pygame.MOUSEMOTION:
                    r.player['a'] += event.rel[0]/200

                if event.type == pygame.QUIT:
                    running= False

            
            fps = str("FPS: "+str(int(clock.get_fps())))
            fps = (pygame.font.SysFont("Arial", 20)).render(fps, 10, pygame.Color("white"))
            screen.blit(fps, (0,475))

            clock.tick(60)
            screen.blit(font.render(str("Tiempo: "+text), 10, pygame.Color("white")), (0, 100))
            pygame.display.update()
        
    """MUSICA DE FONDO"""
    music('./music/MOTOMAMI.mp3')

######################################################### MENU PRINCIPAL
menu = pygame_menu.Menu('MOTO-MAZE', 600, 500, theme=Rosalia_Theme)

menu.add.button('Facil', running, screen, './map3.txt', './music/saoko.mp3')
menu.add.button('Normal', running, screen ,'./map.txt', './music/DIABLO.mp3')
menu.add.button('Dificil', running, screen, './map2.txt', './music/COMOUNG.mp3')

menu.add.button('Cerrar', pygame_menu.events.EXIT, background_color=(0, 0, 0), font_color=(255, 255, 255))

"""MUSICA DE FONDO"""
music('./music/MOTOMAMI.mp3')


menu.mainloop(screen)

