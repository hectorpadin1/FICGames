import pygame as pg
from sprites.character import Character
from pygame.math import Vector2
from settings import *
from math import cos, pi
from control import Controler
from sprites.gun import MachineGun, Pistol, Rifle
from managers.resourcemanager import ResourceManager as GR
from utils.observable import Observable


class Player(Character, Observable):
    #NO ME MOLA NADA COMO SE ESTÁ ACOPLANDO TODO EL JUEGO, MIRAR DE SIMPLEMENTE DAR DE ALTA EL SPRITE
    def __init__(self, x, y, bullets, collide_groups, observers):
        Character.__init__(self, None, GR.PLAYER, PLAYER_HIT_RECT, x, y, PLAYER_HEALTH, collide_groups, GR.HERO_POSITIONS, 4)
        Observable.__init__(self, observers)
        self.last_shot = 0
        pg.mouse.set_pos((x+10) * SPRITE_BOX, y * SPRITE_BOX)
        self.mouse = pg.mouse.get_pos()
        self.controler = Controler()
        self.guns = [Pistol(bullets), Rifle(bullets), MachineGun(bullets)]
        self.gunSelector = 0
        self.shooting = False
        self.reloading = False
        self.last_change = pg.time.get_ticks()
        #Notificamos a observadores inicialización
        self.notify("health", self.health)
        self.notify("gun", self.gunSelector)
        self.notify("ammo", self.guns[self.gunSelector].current_mag)
        self.notify("bullets", self.guns[self.gunSelector].bullets)


    def update_health(self, health):
        if health <= 0:
            self.updateImage(GR.PLAYER_DIE)
            self.health = 0
        else:
            self.health = health
        self.notify("health", self.health)

    def update_ammo(self):
        for gun in self.guns:
                gun.bullets = gun.MAG_SIZE 
        self.notify("bullets", self.guns[self.gunSelector].bullets)

    def __callControler(self):
        # Player dynamics
        self.rot_speed = 0
        self.vel = Vector2(0, 0)
        speed = self.vel.copy()
        # On-Axis movements
        if self.controler.left():
            self.vel.x = -PLAYER_SPEED
        if self.controler.right():
            self.vel.x = PLAYER_SPEED
        if self.controler.up():
            self.vel.y = -PLAYER_SPEED
        if self.controler.down():
            self.vel.y = PLAYER_SPEED
        # Oposite movements
        if self.controler.left() and self.controler.right():
            self.vel.x = 0
        if self.controler.up() and self.controler.down():
            self.vel.y = 0
        # Diagonal movements        
        if self.vel.x!=0 and self.vel.y!=0:
            self.vel *= cos(pi/4)
        
        if  pg.time.get_ticks() - self.last_change > ANIM_DELAY:
            if speed != self.vel:
                self.numImagenPostura = (self.numImagenPostura + 1)%8
            else:
                self.numImagenPostura = 0
            self.last_change = pg.time.get_ticks()
        
        # Switch guns
        if self.controler.switchPistol():
            self.guns[self.gunSelector].cancel_reload()
            self.gunSelector = 0
            self.notify("gun",0)
            self.notify("ammo", self.guns[self.gunSelector].current_mag)
            self.notify("bullets",self.guns[self.gunSelector].bullets)

        if self.controler.switchRiffle():
            self.guns[self.gunSelector].cancel_reload()
            self.gunSelector = 1
            self.notify("gun",1)
            self.notify("ammo", self.guns[self.gunSelector].current_mag)
            self.notify("bullets",self.guns[self.gunSelector].bullets)

        if self.controler.switchMachineGun():
            self.guns[self.gunSelector].cancel_reload()
            self.gunSelector = 2
            self.notify("gun",2)
            self.notify("ammo", self.guns[self.gunSelector].current_mag)
            self.notify("bullets",self.guns[self.gunSelector].bullets)

        # Reload
        if (self.controler.reload()):
            self.guns[self.gunSelector].do_reload()
            self.reloading = True
            self.notify("ammo",-1)

        # Shooting
        if (self.controler.isShooting()):
            self.guns[self.gunSelector].shoot(self.pos, self.rot)
            self.notify("ammo",self.guns[self.gunSelector].current_mag)
            self.notify("bullets",self.guns[self.gunSelector].bullets)



    def update(self, camera_pos, dt):
        self.__callControler()
        # Checks where it has to move
        direction = pg.mouse.get_pos() - Vector2(camera_pos) - self.pos
        self.rot = direction.angle_to(Vector2(1, 0))
        # Moves in time, not in pixels, independent of our frame rate
        self.pos += self.vel * (dt/1000)
        self.guns[self.gunSelector].update()

        if self.health <= 0:
            super().update()
            return

        if self.reloading:
            self.numPostura = 3
            if self.guns[self.gunSelector].reload == False:
                self.notify("ammo",self.guns[self.gunSelector].current_mag)
                self.notify("bullets",self.guns[self.gunSelector].bullets)
                self.reloading = False

        elif self.gunSelector == 0:
            self.numPostura = 1
        elif self.gunSelector == 1:
            self.numPostura = 0
        elif self.gunSelector == 2:
            self.numPostura = 2
        super().update()
        