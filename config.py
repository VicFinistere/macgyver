"""
This is the configuration file use to create and center the screen with title and icon.
"""
import os
import pygame

os.environ["SDL_VIDEO_CENTERED"] = "1"
GAME_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(GAME_DIR, "assets")
ICON_FILE = os.path.join(ASSETS_DIR, "gfx/item.png")
ICON = pygame.image.load(ICON_FILE)
TITLE = 'Mac Gyver'
SCREEN_W = 480
SCREEN_H = 480
SCREEN = pygame.display.set_mode((SCREEN_W, SCREEN_H))
COLORS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "MAROON": (128, 0, 0),
    "RED": (255, 0, 0),
    "BLUE": (0, 0, 255),
    "GREEN": (0, 128, 0),
    "PURPLE": (128, 0, 128),
    "GRAY": (128, 128, 128),
    "SILVER": (192, 192, 192),
    "PINK": (255, 0, 255),
    "YELLOW": (255, 255, 0),
}
