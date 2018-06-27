"""
main.py  : This file plays the game
"""
#! env/bin/python
import pygame
from config import TITLE, ICON
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
pygame.display.set_icon(ICON)


def intro(status):
    """
    Introduction Scene
    :param status: A boolean ready to capture User Event
    :return: Updated Status Param
    """
    current = Intro()
    if current.status:
        status = current.status
    return status


def rules(status):
    """
    Rules Scene
    :param status: A boolean ready to capture User Event
    :return: Updated Status Param
    """
    current = Rules()
    if current.status:
        status = current.status
    return status


def levels(status, level_id, music_status):
    """
    Game Levels
    :param status: (bool) Ready to capture User Event
    :param level_id: (int) for incrementing when passing to another level
    :param music_status: (str) An str working like a bool for music handling between levels
    :return: Updated Status Param + Music Status ( on / off )
    """
    current = Game(level_id, music_status)
    if current.status:
        status = current.status
    return status, current.music_status


def end(status):
    """
    End Scene
    :param status: (bool) Ready to capture User Event
    :return: Updated Status Param
    """
    current = End()
    if current.status:
        status = current.status
    return status


# Game loop
run = True
while run:

    # Splash screen
    play = intro(0)

    # splash screen returns true => rules scene
    if play == 1:
        play = rules(0)

        # if rules scene returns true => game : level 1
        if play == 1:

            #  Play with  music preferences ( "on" by default, only for the first time )
            play, music_status = levels(0, 1, "on")

            # Level one returns true => Check for the others
            if play == 1:
                for level_id in range(2, 4):

                    # Current level returns true : Play another one
                    if play == 1:
                        play, music_status = levels(0, level_id, music_status)

                        # Quit
                        if play == 0:
                            state_id = End()
                            run = False

            else:
                run = False
        else:
            run = False
    else:
        run = False

pygame.quit()
