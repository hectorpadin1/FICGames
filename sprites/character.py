import pygame as pg
from pygame.math import Vector2
from gestorrecursos import GestorRecursos as GR


class Character(pg.sprite.Sprite):
    def __init__(self, groups, img, hit_rect, x, y, health, collide_groups):
        super().__init__(groups)
        self.image_path = img
        self.image = GR.load_image(img)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = hit_rect
        self.hit_rect.center = self.rect.center
        self.vel = Vector2(0, 0)
        self.pos = Vector2(x, y)
        self.rot = 0
        self.health = health
        self.collision_groups = collide_groups
        
    def __collide_hit_rect(self, one, two):
        return one.hit_rect.colliderect(two.rect)

    def __collide_with_walls(self, sprite, group, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(sprite, group, False, self.__collide_hit_rect)
            if hits:
                if hits[0].rect.centerx > sprite.hit_rect.centerx:
                    sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
                if hits[0].rect.centerx < sprite.hit_rect.centerx:
                    sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
                sprite.vel.x = 0
                sprite.hit_rect.centerx = sprite.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(sprite, group, False, self.__collide_hit_rect)
            if hits:
                if hits[0].rect.centery > sprite.hit_rect.centery:
                    sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
                if hits[0].rect.centery < sprite.hit_rect.centery:
                    sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
                sprite.vel.y = 0
                sprite.hit_rect.centery = sprite.pos.y

    def update(self):
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.image = pg.transform.rotate(GR.load_image(self.image_path), self.rot)
        self.hit_rect.centerx = self.pos.x
        for group in self.collision_groups:
            self.__collide_with_walls(self, group, 'x')
        self.hit_rect.centery = self.pos.y
        for group in self.collision_groups:
            self.__collide_with_walls(self, group, 'y')
        self.rect.center = self.hit_rect.center
