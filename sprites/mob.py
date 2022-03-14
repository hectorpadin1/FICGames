import pygame as pg
from sprites.character import Character
from settings import *
from math import pow, sqrt
from pygame.math import Vector2
from sprites.gun import Pistol
from managers.resourcemanager import ResourceManager as GR


class Mob(Character):

    def __init__(self, mob_group, x, y, image, gun, collide_groups, row, area):
        super().__init__(mob_group, image, MOB_HIT_RECT.copy(), x, y, MOB_HEALTH, collide_groups, GR.MOB_POSITIONS, row)
        self.acc = Vector2(0, 0)
        self.gun = gun
        self.last_shot = pg.time.get_ticks()
        self.reloading = False
        self.dead = False
        self.area = area
        self.activated = False
        self.last_change = pg.time.get_ticks()
    
    def activate(self, area):
        if self.area == area:
            self.moving = True   

    def update(self):
        # Shooting
        # provisional
        if not self.dead:
            if not self.reloading and self.gun.current_mag == 0:
                self.gun.do_reload()
                self.reloading = True
            elif self.moving and self.gun.current_mag != 0:
                self.reloading = False
                self.gun.shoot(self.pos, self.rot)
            self.gun.update()
        super().update()


class MobBasico(Mob):
    
    def __init__(self, mob_group, x, y, bullets, collide_groups, area):
        gun = Pistol(bullets)
        super().__init__(mob_group, x, y, GR.MOB, gun, collide_groups, 1, area)

    def die(self):
        self.updateImage(GR.MOB_DIE)
        self.dead = True     

    def update(self, player_pos, dt):
        if not self.dead:
            distance = sqrt(pow(player_pos.x - self.pos.x, 2) + pow(player_pos.x - self.pos.x, 2))
            if not self.moving:
                self.numImagenPostura = 0
                return
            if distance > MOB_ATTK_DISTANCE*4:
                self.moving = False
                self.numImagenPostura = 0
                return
            if  pg.time.get_ticks() - self.last_change > ANIM_DELAY:
                self.numImagenPostura = (self.numImagenPostura + 1)%8
                self.last_change = pg.time.get_ticks()
            self.moving = True
            self.rot = (player_pos - self.pos).angle_to(Vector2(1, 0))
            if distance > MOB_ATTK_DISTANCE/2:
                self.acc = Vector2(MOB_SPEED, 0).rotate(-self.rot)
                self.acc += self.vel * -1
                self.vel += self.acc * (dt/1000)
                self.pos += self.vel * (dt/1000) + 0.5 * self.acc * (dt/1000) ** 2
        super().update()
