'''
Andrew ID: wzhao3

Main program run code
'''

import pygame
import sys
from eventController import *

pygame.init()


def play(width, height):
    # size = (800, 800)
    size = (width, height)
    # screen = pygame.display.set_mode(size)
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    pygame.display.set_caption('Renegade Starship')
    clock = pygame.time.Clock()

    frameRate = 60

    #Struct class partially taken from 112 course notes
    class Struct(object):
        pass
    data = Struct()
    data.width = size[0]
    data.height = size[1]
    init(data)
    done = False

    while not done:
        black = (0, 0, 0)
        screen.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                keyPressed(event, data)
            if event.type == pygame.KEYUP:
                keyReleased(event, data)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePressed(data)
            if event.type == pygame.MOUSEBUTTONUP:
                mouseReleased(data)
            if event.type == pygame.MOUSEMOTION:
                mouseMoved(data)
            pass

        timerFired(data)
        redrawAll(screen, data)

        data.timer += 1
        clock.tick(frameRate)
        pygame.display.flip()

    pygame.quit()

play(1280, 800)

sys.exit()