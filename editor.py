import inspect
import os
from random import random

import numpy as np
import pygame
# recherche du répertoire de travail
from pygame import draw, transform, surfarray
from pygame.rect import Rect
from pygame.transform import scale

from common import WHITE, palette

pixel_size = 40
terrain_dim = [20, 15]

void = pygame.Surface((94, 94))
void.fill(WHITE)

###################################################################################

# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [pixel_size * (terrain_dim[0] + 1), pixel_size * terrain_dim[1]]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Map editor")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

pygame.mouse.set_visible(1)

matrice = []
for line in range(terrain_dim[1]):
    chaine = ""
    for col in range(terrain_dim[0]):
        chaine = chaine + " "
    matrice.append(chaine)

select = 'P'

while not done:

    time = int(pygame.time.get_ticks() / 100)

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loo

    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        print("x:" + str(x) + " y:" + str(y))
        if x // pixel_size < terrain_dim[0]:
            array = bytearray(matrice[y // pixel_size], 'UTF-8')
            array[x // pixel_size] = int.from_bytes(select.encode('UTF-8'), "big")
            matrice[y // pixel_size] = str(array.decode('UTF-8'))
        else:
            try:
                select = palid[y // pixel_size]
                if select == "EXPORT":
                    select = ' '
                    print("Map :")
                    for ligne in matrice:
                        print("\"{}\",".format(ligne))
                        clicked = False
                elif select == "RANDOM":
                    select = ' '
                    matrice = []
                    for line in range(terrain_dim[1]):
                        chaine = ""
                        for col in range(terrain_dim[0]):
                            chaine = chaine + palid[int(random() * 6)]
                        matrice.append(chaine)
                    clicked = False
            except:
                ""

    # draw background
    screen.fill(WHITE)

    LABY = np.zeros((terrain_dim[0], terrain_dim[1]), pygame.Surface)
    for y in range(terrain_dim[1]):
        ligne = matrice[y]
        for x in range(terrain_dim[0]):
            c = ligne[x]
            LABY[x, y] = palette[c]

    for ix in range(terrain_dim[0]):
        for iy in range(terrain_dim[1]):
            xpix = pixel_size * ix
            ypix = pixel_size * iy
            couleur = LABY[ix, iy]
            screen.blit(scale(palette['P'], (pixel_size, pixel_size)), (xpix, ypix))
            screen.blit(scale(couleur, (pixel_size, pixel_size)), (xpix, ypix))
            # pygame.draw.rect(screen, couleur, [xpix, ypix, pixel_size, pixel_size])

    palid = {}
    i = 0
    for coul in palette:
        xpix = pixel_size * terrain_dim[0]
        ypix = pixel_size * i
        couleur = palette[coul]
        palid[i] = coul
        screen.blit(scale(palette['P'], (pixel_size, pixel_size)), (xpix, ypix))
        screen.blit(scale(couleur, (pixel_size, pixel_size)), (xpix, ypix))
        i = i + 1

    clock.tick(20)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

pygame.quit()
