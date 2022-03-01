from pygame import Rect
from pygame.math import Vector2

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# General game setings
TITLE = "Juego Molón que mola un montón"
WIDTH = 1024  # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768 # 16 * 48 or 32 * 24 or 64 * 12
FPS = 120
SPRITE_BOX = 64
GRIDWIDTH = WIDTH / SPRITE_BOX
GRIDHEIGHT = HEIGHT / SPRITE_BOX


# MUSIC    
START_MUSIC = 'resources/music/start_background.mp3'
MAIN_MUSIC  = 'resources/music/main_background.ogg'

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 300.0
PLAYER_ROT_SPEED = 250.0
PLAYER_HIT_RECT = Rect(0, 0, 35, 35)
BARREL_OFFSET = Vector2(20, 3)

# Settings for Shootings
BULLET_SPEED = 1500
BULLET_LIFETIME = 2000
BULLET_RATE = 10
KICKBACK = 200
GUN_SPREAD = 5
EXPLOSION_LIFETIME = 100
BULLET_DAMAGE = 10

# Mob Settings
MOB_SPEED = 150
MOB_HIT_RECT = Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
BLOOD_LIFETIME = 10000

# Gui Sizes
GUI_BOX_SIZE = (384,448)
GUI_FONT_SIZE = 20
GUI_COLOR = (18,17,16)