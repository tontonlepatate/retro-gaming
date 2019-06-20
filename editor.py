import inspect
import os
from random import random

import numpy as np
import pygame
# recherche du répertoire de travail
from pygame import draw, transform, surfarray, Surface
from pygame.draw import rect
from pygame.rect import Rect
from pygame.transform import scale

from common import WHITE, palette, YELLOW, BLACK, RED

pixel_size = 40
terrain_dim = [20, 15]

void = pygame.Surface((94, 94))
void.fill(WHITE)

###################################################################################

# Initialize pygame
pygame.init()

police = pygame.font.SysFont("arial", 15, True)

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [pixel_size * (terrain_dim[0] + 1), pixel_size * (terrain_dim[1] + 1)]
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
    pos = pygame.mouse.get_pos()
    x = pos[0] // pixel_size
    y = pos[1] // pixel_size

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loo

        if event.type == pygame.MOUSEBUTTONDOWN:
            if y >= terrain_dim[1]:
                btn_generer = Rect((terrain_dim[0] - 1), terrain_dim[1], 2, 1)
                btn_aleatoire = Rect((terrain_dim[0] - 3), terrain_dim[1], 2, 1)
                if btn_generer.collidepoint(x, y):
                    select = ' '
                    print("Map :")
                    for ligne in matrice:
                        print("\"{}\",".format(ligne))

                elif btn_aleatoire.collidepoint(x, y):
                    select = ' '
                    matrice = []
                    base_count = 0
                    for line in range(terrain_dim[1]):
                        chaine = ""
                        for col in range(terrain_dim[0]):
                            letter = palid[int(random() * 6)]
                            while letter == 'B':
                                letter = palid[int(random() * 6)]
                            chaine = chaine + letter

                        matrice.append(chaine)

            elif x >= terrain_dim[0]:
                select = palid[y]

    if pygame.mouse.get_pressed()[0]:

        if x < terrain_dim[0] and y < terrain_dim[1]:
            array = bytearray(matrice[y], 'UTF-8')
            array[x] = int.from_bytes(select.encode('UTF-8'), "big")
            matrice[y] = str(array.decode('UTF-8'))

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

    # Affichage bouton TOUR SUIVANT
    btn_toursuiv = Surface((pixel_size * 2, pixel_size))
    btn_toursuiv.fill(YELLOW)
    text = police.render("Génerer", True, BLACK)
    text = transform.scale(text, (pixel_size * 2, pixel_size))
    btn_toursuiv.blit(text, (0, 0))
    screen.blit(btn_toursuiv, ((terrain_dim[0] - 1) * pixel_size, terrain_dim[1] * pixel_size))

    # Affichage bouton TOUR SUIVANT
    btn_toursuiv = Surface((pixel_size * 2, pixel_size))
    btn_toursuiv.fill(RED)
    text = police.render("Aleatoire", True, BLACK)
    text = transform.scale(text, (pixel_size * 2, pixel_size))
    btn_toursuiv.blit(text, (0, 0))
    screen.blit(btn_toursuiv, ((terrain_dim[0] - 3) * pixel_size, terrain_dim[1] * pixel_size))

    clock.tick(20)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

pygame.quit()
