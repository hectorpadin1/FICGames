import os
import pygame as pg
import pytmx

#DEBUGUEAR PARA COMPROBAR QUE SE ACTUALIZAN LAS LISTAS SIENDO ESTATICO

class ResourceManager:
    image_resources = {}
    map_resources   = {}
    font_resources  = {}
    sound_resources = {}

    # SPRITE IMAGES 
    PLAYER_RIFFLE   = 'images-sprites/Hero_Rifle.png'
    PLAYER_PISTOL   = 'images-sprites/Hero_Pistol.png'
    PLAYER_MACHINEGUN   = 'images-sprites/Hero_MachineGun.png'
    PLAYER_RELOAD   = 'images-sprites/Hero_Reload.png'
    PLAYER_DIE      = 'images-sprites/Hero_Die.png'
    BULLET_IMG      = 'images-sprites/bullet.png'
    EXPLOSION_IMAGE = 'images-sprites/explode_bullet.png'
    MOB_IMAGE       = 'images-sprites/soldier.png'
    BLOOD_IMAGE     = 'images-sprites/blood.png'
    HIT_IMAGE     = 'images-sprites/blood-splatter.png'
    
    # GUI IMAGES
    LOGO_IMG     = 'images-gui/logo.png'
    START_IMG    = 'images-gui/inicio.png'
    BTN_BG       = 'images-gui/btn_bg.png'
    BOX_BG       = 'images-gui/box_bg.png'
    GAMEOVER_IMG = 'images-gui/gameover.png'
    PAUSE_IMG    = 'images-gui/pause.png'
    LVL_BTN      = 'images-gui/lvl_btn.png'
    SELECT_LOGO  = 'images-gui/select_level_logo.png'
    HUD          = 'images-gui/hud.png'
    PISTOLHUD    = 'images-gui/pistolhud.png'
    SMGHUD       = 'images-gui/smghud.png'
    MGHUD        = 'images-gui/mghud.png'

    # FONTS
    MAIN_FONT = "fonts/ModernDOS9x16.ttf"

    # SOUNDS
    SELECTION     = 'sound_effects/selection.mp3'
    METRALLETA    = 'sound_effects/metralleta.mp3'
    AMETRALLADORA = 'sound_effects/ametralladora.mp3'
    PISTOLA       = 'sound_effects/pistola.mp3'

    # MAPS
    LEVEL = ['maps/level0.tmx','maps/level1.tmx','maps/level2.tmx','maps/level3.tmx','maps/level4.tmx']

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