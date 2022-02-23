from pygame import Rect
from pygame.math import Vector2

# General game setings
TITLE = "Juego Molón que mola un montón"
WIDTH = 1024  # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768 # 16 * 48 or 32 * 24 or 64 * 12
FPS = 30
SPRITE_BOX = 64
GRIDWIDTH = WIDTH / SPRITE_BOX
GRIDHEIGHT = HEIGHT / SPRITE_BOX

# MAPS
LEVEL1 = 'maps/level1.tmx'

#FONTS
MAIN_FONT = "assets/ModernDOS9x16.ttf"

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 300.0
PLAYER_ROT_SPEED = 250.0
PLAYER_IMG = 'assets/soldier.png'
PLAYER_HIT_RECT = Rect(0, 0, 35, 35)
BARREL_OFFSET = Vector2(20, 3)

# Settings for Shootings
BULLET_IMG = 'assets/bullet.png'
EXPLOSION_IMAGE = 'assets/explode_bullet.png'
BULLET_SPEED = 1000
BULLET_LIFETIME = 2000
BULLET_RATE = 150
KICKBACK = 200
GUN_SPREAD = 5
EXPLOSION_LIFETIME = 100
BULLET_DAMAGE = 10

# Mob Settings
MOB_IMAGE = 'assets/soldier.png'
MOB_SPEED = 150
MOB_HIT_RECT = Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20

# Gui Assets
LOGO_IMG = 'assets/logo.png'
BTN_BG = 'assets/btn_bg.png'
BOX_BG = 'assets/box_bg.png'

# Gui Sizes
GUI_BOX_SIZE = (384,448)
GUI_FONT_SIZE = 20
GUI_COLOR = (18,17,16)