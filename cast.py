import pygame
from math import *
import pygame_menu
from pygame import mixer
from Raycaster import *

BLACK = (0,0,0)
WHITE = (255,255,255)
SKY = (40,100,200)
GROUND = (200,200,100)
TRANSPARENT = (152,0,136,255)

def music(music):
    """MUSICA DE FONDO"""
    mixer.music.stop()
    mixer.music.load(music)
    mixer.music.play(-1)
    mixer.music.set_volume(0.1)
    """MUSICA DE FONDO"""

def FPS():
    fps = str("FPS: "+str(int((pygame.time.Clock()).get_fps())))
    fps = (pygame.font.SysFont("Arial", 20)).render(fps, 10, pygame.Color("white"))
    return fps

def running(screen, map, musica):
    r = Raycaster(screen)
    r.load_map(map)

    music(musica)

    running = True
    while running:
        screen.fill(BLACK,(0,0,r.width,r.height))
        screen.fill(SKY,(r.width/2,0,r.width,r.height/2))
        screen.fill(GROUND, (r.width/2,r.height/2,r.width,r.height/2))
        r.render()
        r.clearZ()

        screen.blit(FPS(), (0,475))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running= False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                r.player['a'] -= pi/10
            if keys[pygame.K_d]:
                r.player['a'] += pi/10

            if keys[pygame.K_RIGHT]:
                r.player['x'] += 10
            if keys[pygame.K_LEFT]:
                r.player['x'] -= 10
            if keys[pygame.K_UP]:
                r.player['y'] -= 10
            if keys[pygame.K_DOWN]:
                r.player['y'] += 10
    
    """MUSICA DE FONDO"""
    music('./music/MOTOMAMI.mp3')
    """MUSICA DE FONDO"""

pygame.init()
screen = pygame.display.set_mode((1000,500))

######################################################### THEME MENU PRINCIPAL
myimage = pygame_menu.baseimage.BaseImage(
    image_path = './imagenes/rosalia.jpg',
    drawing_mode = pygame_menu.baseimage.IMAGE_MODE_FILL,
)

Theme = pygame_menu.themes.Theme
Rosalia_Theme = Theme(background_color = myimage,
                title_background_color = (116, 0, 1),
                title_font = pygame_menu.font.FONT_FRANCHISE,
                title_font_size = 100,
                title_offset = (335, 0),

                cursor_selection_color = (255, 255, 255),

                widget_font = pygame_menu.font.FONT_FRANCHISE,
                widget_alignment = pygame_menu.locals.ALIGN_CENTER,
                widget_font_color=(0, 0, 0),
                widget_background_color=(116, 0, 1),
                widget_padding = (10,20),
                widget_margin = (0,20))
                

######################################################### MENU PRINCIPAL
menu = pygame_menu.Menu('Rosa-Killa', 1000, 500, theme=Rosalia_Theme)

menu.add.button('Nivel 1', running, screen ,'./map.txt', './music/DIABLO.mp3')
menu.add.button('Nivel 2', running, screen, './map2.txt', './music/COMOUNG.mp3')
menu.add.button('Cerrar', pygame_menu.events.EXIT)

"""MUSICA DE FONDO"""
music('./music/MOTOMAMI.mp3')
"""MUSICA DE FONDO"""

menu.mainloop(screen, fps_limit=60.0)

