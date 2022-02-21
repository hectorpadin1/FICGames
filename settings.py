from pygame import Rect

# General game setings
TITLE = "Juego Molón que mola un montón"
WIDTH = 1024  # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768 # 16 * 48 or 32 * 24 or 64 * 12
FPS = 30
SPRITE_BOX = 64
GRIDWIDTH = WIDTH / SPRITE_BOX
GRIDHEIGHT = HEIGHT / SPRITE_BOX

# Player settings
PLAYER_SPEED = 300.0
PLAYER_ROT_SPEED = 250.0
PLAYER_IMG = 'assets/topdown-shooter/PNG/Hitman 1/hitman1_gun.png'
PLAYER_HIT_RECT = Rect(0, 0, 35, 35)

# Settings for Shootings
BULLET_IMG = ''
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = 150

# Gui Assets
LOGO_IMG = 'assets/logo.png'
BTN_BG = 'assets/btn_bg.png'
BOX_BG = 'assets/box_bg.png'

# Gui Sizes
GUI_BOX_SIZE = (384,448)
GUI_FONT_SIZE = 20
GUI_COLOR = (18,17,16)