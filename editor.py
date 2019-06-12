import inspect
import os
from random import random

import numpy as np
import pygame
# recherche du répertoire de travail
from pygame import draw, transform, surfarray
from pygame.rect import Rect

BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255)

palette = {
    'B': [0, 0, 255],
    ' ': [0, 0, 0],
    'W': [255, 255, 255],
    'G': [0, 255, 0],
    'R': [255, 0, 0],
    'Y': [255, 255, 0],
    'C': [0, 225, 255],
    'EXPORT': [100, 100, 100]
}  # initialise un dictionnaire

LARG = 20

###################################################################################

# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [LARG * 21, LARG * 20]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("LEMMINGS")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

pygame.mouse.set_visible(1)

matrice = ['                    ',
           '                    ',
           '                    ',
           '                    ',
           '                    ',
           '                    ',
           '                    ',
           '                    ',
           '                    ',
           '                    ',
           '                    ',
           '                    ',
           '                    ',
           '                    ',
           '                    ',
           '                    ',
           '                    ',
           '                    ',
           '                    ',
           '                    ']

select = 'B'
clicked = False

while not done:
    event = pygame.event.Event(pygame.USEREVENT)  # Remise à zero de la variable event

    time = int(pygame.time.get_ticks() / 100)

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    # draw background
    screen.fill(WHITE)

    if select == "EXPORT":
        select = ' '
        for ligne in matrice:
            print("\"{}\",".format(ligne))

    LABY = np.zeros((20, 20, 3))
    for y in range(20):
        ligne = matrice[y]
        for x in range(20):
            c = ligne[x]
            LABY[x, y] = palette[c]

    for ix in range(20):
        for iy in range(20):
            xpix = LARG * ix
            ypix = LARG * iy
            couleur = LABY[ix, iy]
            pygame.draw.rect(screen, couleur, [xpix, ypix, LARG, LARG])

    palid = {}
    i = 0
    for coul in palette:
        xpix = LARG * 20
        ypix = LARG * i
        couleur = palette[coul]
        palid[i] = coul
        pygame.draw.rect(screen, couleur, [xpix, ypix, LARG, LARG])
        i = i + 1

    if event.type == pygame.MOUSEBUTTONDOWN:
        clicked = True
    elif event.type == pygame.MOUSEBUTTONUP:
        clicked = False

    if clicked is True:
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        if x // 20 < 19:
            array = bytearray(matrice[y // 20], 'UTF-8')
            array[x // 20] = int.from_bytes(select.encode('UTF-8'), "big")
            matrice[y // 20] = str(array.decode('UTF-8'))
        else:
            try:
                select = palid[y // 20]
            except:
                ""

    clock.tick(20)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

pygame.quit()
