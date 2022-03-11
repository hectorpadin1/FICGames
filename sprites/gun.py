import pygame as pg
from settings import *
from resourcemanager import ResourceManager as GR
from sprites.bullet import Bullet
from soundcontroller import SoundController as SC


class AbstractGun():
    
    def __init__(self, bullet_group, ammo, bullet_img, reload_time, rate, damage, speed, lifetime, soundFunction):
        self.bullet_group = bullet_group
        self.MAX_AMMO = ammo
        self.ammo = ammo
        self.reload_time = reload_time
        self.bullet_img = bullet_img
        self.rate = rate
        self.speed = speed
        self.lifetime = lifetime
        self.last_shot = pg.time.get_ticks()
        self.damage = damage
        self.soundFunction = soundFunction
        self.reload = False
    
    def shoot(self, pos, rot):
        if self.ammo == 0:
            self.reload = True
        if not self.reload:
            now = pg.time.get_ticks()
            if now - self.last_shot > self.rate:
                self.last_shot = now
                self.ammo -= 1
                Bullet(self.bullet_group, pos, rot, self.bullet_img, self.speed, self.lifetime)
                self.soundFunction()
    
    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.reload_time:
            self.ammo = self.MAX_AMMO
            self.reload = False


class Pistol(AbstractGun):

    def __init__(self, bullet_group):
        super().__init__(bullet_group, 7, GR.BULLET_IMG, 20*FPS, 4*FPS, 34, 1500, 2*FPS, SC.play_pistola)


class Rifle(AbstractGun):

    def __init__(self, bullet_group):
        super().__init__(bullet_group, 30, GR.BULLET_IMG, 30*FPS, 1*FPS, 40, 2000, 5*FPS, SC.play_metralleta)


class MachineGun(AbstractGun):

    def __init__(self, bullet_group):
        super().__init__(bullet_group, 100, GR.BULLET_IMG, 100*FPS, 30, 30, 2000, 3*FPS, SC.play_ametralladora)
    
