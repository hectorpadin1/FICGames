import os
import pygame as pg
import pytmx

#DEBUGUEAR PARA COMPROBAR QUE SE ACTUALIZAN LAS LISTAS SIENDO ESTATICO

class GestorRecursos:
    image_resources = {}
    map_resources   = {}
    font_resources  = {}
    sound_resources = {}

    # SPRITE IMAGES 
    PLAYER_IMG      = 'images-sprites/soldier.png'
    BULLET_IMG      = 'images-sprites/bullet.png'
    EXPLOSION_IMAGE = 'images-sprites/explode_bullet.png'
    MOB_IMAGE       = 'images-sprites/soldier.png'
    BLOOD_IMAGE     = 'images-sprites/blood.png'
    HIT_IMAGE     = 'images-sprites/blood-splatter.png'
    
    # GUI IMAGES
    LOGO_IMG = 'images-gui/logo.png'
    BTN_BG   = 'images-gui/btn_bg.png'
    BOX_BG   = 'images-gui/box_bg.png'

    # FONTS
    MAIN_FONT = "fonts/ModernDOS9x16.ttf"

    # SOUNDS
    SELECTION   = 'sound_effects/selection.mp3'
    METRALLETA  = 'sound_effects/metralleta.mp3'

    # MAPS
    LEVEL1 = 'maps/level1.tmx'
    LEVEL2 = 'maps/level2.tmx'
    LEVEL3 = 'maps/level3.tmx'
    LEVEL4 = 'maps/level4.tmx'
    LEVEL5 = 'maps/level5.tmx'
    LEVEL6 = 'maps/level6.tmx'

    # PATHS
    RESOURCE_PATH = "resources"

    @classmethod
    def load_image(self, nombre):
        if nombre in self.image_resources:
            return self.image_resources[nombre]
        else:
            fullname = os.path.join(self.RESOURCE_PATH, nombre)
            try:
                imagen = pg.image.load(fullname)
            except (pg.error):
                print('Cannot load image: ', fullname)
                raise SystemExit

            imagen = imagen.convert_alpha() # o convert_alpha??
            
            self.image_resources[nombre] = imagen
            
            return imagen

    @classmethod
    def load_map(self, nombre):
        if nombre in self.map_resources:
            return self.map_resources[nombre]
        else:
            tm = pytmx.load_pygame(os.path.join(self.RESOURCE_PATH, nombre), pixelalpha=True)
            self.map_resources[nombre] = tm    
            return tm

    @classmethod
    def load_font(self, nombre, size):
        if (nombre,size) in self.font_resources:
            return self.font_resources[(nombre,size)]
        else:
            fullname = os.path.join(self.RESOURCE_PATH, nombre)
            try:
                font = pg.font.Font(fullname,size)
            except (pg.error):
                print('Cannot load font: ', fullname)
                raise SystemExit

            self.font_resources[(nombre,size)] = font
            return font

    @classmethod
    def load_sound(self, nombre):
        if nombre in self.sound_resources:
            return self.sound_resources[nombre]
        else:
            fullname = os.path.join(self.RESOURCE_PATH, nombre)
            try:
                sound = pg.mixer.Sound(fullname)
            except (pg.error):
                print('Cannot load sound: ', fullname)
                raise SystemExit

            self.sound_resources[nombre] = sound
            return sound