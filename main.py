#! env/bin/python
import pygame
from config import TITLE
from intro import Intro
from game import Game
from end import End

pygame.init()
pygame.font.init()
pygame.mixer.init()


if not pygame.font:
    print('Warning, fonts disabled')

if not pygame.mixer:
    print('Warning, sound disabled')

pygame.display.set_caption(TITLE)

play = Intro()
if play.state == 1:
    play = Game()

play = End()
pygame.quit()
