import pygame as pg
from settings import *
from pygame.math import Vector2
from sprites.explosion import *
from managers.resourcemanager import ResourceManager as GR


class Bullet(pg.sprite.Sprite):
    
    def __init__(self, bullet_group, pos, rot, img, speed, lifetime):
        pg.sprite.Sprite.__init__(self, bullet_group)
        dir = Vector2(1, 0).rotate(-rot)
        self.image = GR.load_image(img,-1).convert_alpha()
        self.image = pg.transform.rotate(self.image, rot-90)
        self.rect = pg.Rect((0,0), (19, 5))
        self.pos = Vector2(pos)

        data = GR.load_coord(GR.BULLET_POSITIONS)
        data = data.split()
        self.numPostura = 0
        self.numImagenPostura = 0
        cont = 0
        numImagenes = [3]
        self.coordenadasHoja = []
        for linea in range(0, 1):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea]+1):
                tmp.append(pg.Rect((int(data[cont]), int(data[cont+1])), (int(data[cont+2]), int(data[cont+3]))))
                cont += 4
        print(self.coordenadasHoja[0][0])
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = pos
        self.vel = dir * speed
        self.lifetime = lifetime
        self.spawn_time = pg.time.get_ticks()

    def update(self, dt):
        self.pos += self.vel * (dt/1000)
        self.rect.center = self.pos
        now = pg.time.get_ticks() - self.spawn_time
        if now > 2*self.lifetime/3 and self.numImagenPostura==1:
            self.numImagenPostura += 1
        elif now > self.lifetime/3 and self.numImagenPostura==0:
            self.numImagenPostura += 1
        if now > self.lifetime:
            self.kill()
    