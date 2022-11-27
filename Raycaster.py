import pygame
from math import *
import pygame_menu

BLACK = (0,0,0)
WHITE = (255,255,255)

SKY = (40,100,200)
GROUND = (200,200,100)

TRANSPARENT = (152,0,136,255)

colors = [
    (0,20,10),
    (4,40,63),
    (0,91,82),
    (219,248,38),
    (2,248,50),
]

walls = {
    '1': pygame.image.load('./wall/wall1.png'),
    '2': pygame.image.load('./wall/wall2.png'),
    '3': pygame.image.load('./wall/wall3.png'),
    '4': pygame.image.load('./wall/wall4.png'),
    '5': pygame.image.load('./wall/wall5.png'),
}

sprite1= pygame.image.load('./sprite/sprite1.png')
sprite2= pygame.image.load('./sprite/sprite2.png')
sprite3= pygame.image.load('./sprite/sprite3.png')
sprite4= pygame.image.load('./sprite/sprite4.png')

enemies = [
    {
        'x':100,
        'y':150,
        'sprite': sprite1,
    },
    {
        'x':300,
        'y':300,
        'sprite': sprite2,
    },
]

class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height= screen.get_rect()
        self.blocksize = 50
        self.map = []
        self.player = {
            'x': int(self.blocksize + self.blocksize / 2),
            'y': int(self.blocksize + self.blocksize / 2),
            'fov': int(pi/3),
            'a': int(pi/3),
        }
        self.clearZ()

    def clearZ(self):
        self.zbuffer = [9999 for z in range(0,self.width)]

    def point(self, x, y, c=WHITE):
        self.screen.set_at((x,y),c)

    def block(self, x,y, wall):
        for i in range(x,x + self.blocksize):
            for j in range(y,y + self.blocksize):
                tx = int((i - x) * 128 / self.blocksize)
                ty = int((j - y) * 128 / self.blocksize)
                c = wall.get_at((tx,ty))
                self.point(i,j,c)

    def block2(self, x,y, wall):
        for i in range(x,x + 10):
            for j in range(y,y + 10):
                tx = int((i - x) * 128 /10)
                ty = int((j - y) * 128 / 10)
                c = wall.get_at((tx,ty))
                self.point(i,j,c)

    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

    def draw_stake(self,x,h,c,tx):
        start_y = int(self.height/2 - h/2)
        end_y = int(self.height/2 + h/2)
        height = end_y - start_y

        for y in range(start_y,end_y):
            ty = int((y-start_y) * 128 / height)
            color = walls[c].get_at((tx,ty))
            self.point(x,y,color)

    def cast_ray(self, a):
        d = 0
        ox = self.player['x']
        oy = self.player['y']
        
        while True:
            x = int(ox + d * cos(a))
            y = int(oy + d * sin(a))

            i = int(x / self.blocksize)
            j = int(y / self.blocksize)

            if self.map[j][i] != ' ':
                hitx = x -i*self.blocksize
                hity = y -j*self.blocksize

                if 1 < hitx < self.blocksize - 1:
                    maxhit = hitx
                else:
                    maxhit = hity

                tx = int(maxhit * 128 / self.blocksize)
                return d, self.map[j][i], tx

            self.point(x,y)
            d += 1
    
    def draw_map(self):
        size = 10
        for x in range(0,100,size):
            for y in range(0,100,size):
                i = int(x / size)
                j = int(y / size)
                
                if self.map[j][i] != ' ':
                    if self.map[j][i] != '\n':
                        self.block2(x,y, walls[self.map[j][i]])
                
    def draw_player(self):
        try:
            self.point(self.player['x'],self.player['y'])
        except:
            pass

    def draw_sprite(self,sprite):
        sprite_a = atan2(sprite['y'] - self.player['y'],sprite['x'] - self.player['x'],)
        
        d = ((self.player['x']-sprite['x'])**2 + (self.player['y'] - sprite['y'])**2)**0.5

        sprite_size = int(500/d * (500/10))

        sprite_x = int(
            500 +
            (sprite_a - self.player['a']) * 500/ self.player['fov'] 
            + sprite_size/2
        )
        sprite_y = int(500/2 - sprite_size/2)
        
        for x in range(sprite_x,sprite_x+sprite_size):
            for y in range(sprite_y,sprite_y+sprite_size):
                tx = int((x - sprite_x) * 128/sprite_size)
                ty = int((y-sprite_y) * 128/sprite_size)
                c = sprite['sprite'].get_at((tx,ty))
                if c != TRANSPARENT:
                    if x> 500:
                        if self.zbuffer[x-500] >= d:
                            self.point(x,y,c)
                            self.zbuffer[x - 500] = d

    def render(self):
        self.draw_map()
        self.draw_player()

        density = 10
        for i in range(0,density):
            a = self.player['a'] - self.player['fov']/2 + self.player['fov'] * i/density
            d,c, _ = self.cast_ray(a)

        for i in range(0,500):
            self.point(499,i)
            self.point(500,i)
            self.point(501,i)

        for i in range(0,int(self.width/2)):
            a = self.player['a'] - self.player['fov']/2 + self.player['fov'] * i/(self.width/2)
            d,c,tx = self.cast_ray(a)

            x = int(self.width/2) + i
            h = self.height/(d * cos(a - self.player['a'])) * self.height /10

            if self.zbuffer[i] >= d:
                self.draw_stake(x,h,c,tx)
                self.zbuffer[i] = d
        

        for enemy in enemies:
            self.draw_sprite(enemy)