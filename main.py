#! env/bin/python
import pygame
from config import TITLE
from intro import Intro
from rules import Rules
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


def intro(status):
    play = Intro()
    if play.status:
        status = play.status
    return status


def rules(status):
    play = Rules()
    if play.status:
        status = play.status
    return status


def levels(status, level_id, music_status):
    play = Game(level_id, music_status)
    if play.status:
        status = play.status
    return status, play.music_status


def end(status):
    play = End()
    if play.status:
        status = play.status
    return status


run = True
while run:
    # Splash screen
    if run:
        state_id = intro(0)

    # Game active / splash screen
    if state_id == 1:
        state_id = rules(0)

        # Game active / rules
        if state_id == 1:
            state_id, music_status = levels(0, 1, "on")

            # Game active / first level
            if state_id == 1:
                for level_id in range(2, 4):

                    # Game active / game
                    if state_id == 1:
                        state_id, music_status = levels(0, level_id, music_status)

                        # End
                        if state_id == 0:
                            state_id = End()
                            run = False

                    # Quit before end
                    elif state_id == 0:
                        # End Screen
                        state_id = End()
                        run = False

            else:
                run = False
        else:
            run = False
    else:
        run = False

pygame.quit()
