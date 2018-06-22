import pygame
import os
os.environ["SDL_VIDEO_CENTERED"] = "1"
GAME_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(GAME_DIR, "assets")
TITLE = 'Mac Gyver'
WIDTH = 480
HEIGHT = 480
ENEMY_POS= (200, 200)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
score = open('score.txt', 'w')
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
    "YELLOW": (255,255,0),
}


