import inspect
import os
from random import random

import numpy as np
import pygame
# recherche du répertoire de travail
from pygame import draw, transform, surfarray
from pygame.rect import Rect
from pygame.transform import scale

pixel_size = 40
terrain_dim = [20, 15]

scriptPATH = os.path.abspath(inspect.getsourcefile(lambda: 0))  # compatible interactive Python Shell
scriptDIR = os.path.dirname(scriptPATH)
assets = os.path.join(scriptDIR, "data")

image1_sprites = pygame.image.load(os.path.join(assets, "World_A1.png"))
image2_sprites = pygame.image.load(os.path.join(assets, "World_A2.png"))
image3_sprites = pygame.image.load(os.path.join(assets, "World_B.png"))
image4_sprites = pygame.image.load(os.path.join(assets, "World_C.png"))


def charger_sprite(feuille, x, y, size):
    planche_sprites = feuille
    planche_sprites.set_colorkey((0, 0, 0))
    return planche_sprites.subsurface((x, y, size, size))


BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255)

void = pygame.Surface((94, 94))
void.fill(WHITE)

palette = {
    'B': charger_sprite(image3_sprites, 383, 0, 95),  # base
    'E': charger_sprite(image1_sprites, 23, 70, 50),  # eau
    'R': charger_sprite(image2_sprites, 13, 210, 50),  # route
    'V': charger_sprite(image4_sprites, 0, 334, 95),  # ville
    'f': charger_sprite(image2_sprites, 378, 48, 95),  # foret
    'S': charger_sprite(image2_sprites, 490, 220, 50),  # plage
    'M': charger_sprite(image2_sprites, 671, 47, 95),  # montagne
    'C': charger_sprite(image2_sprites, 576, 47, 95),  # colline
    'P': charger_sprite(image2_sprites, 211, 70, 50),  # plaine
    'F': charger_sprite(image3_sprites, 673, 100, 95),  # fort
    'T': charger_sprite(image4_sprites, 470, 188, 95),  # recherche
    'U': charger_sprite(image4_sprites, 376, 188, 95),  # Usine M
    'u': charger_sprite(image4_sprites, 376, 282, 95),  # Usine C
    ' ': charger_sprite(image2_sprites, 211, 70, 50)
}  # initialise un dictionnaire

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
clicked = False

while not done:
    event = pygame.event.Event(pygame.USEREVENT)  # Remise à zero de la variable event

    time = int(pygame.time.get_ticks() / 100)

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

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

    if event.type == pygame.MOUSEBUTTONDOWN:
        clicked = True
    elif event.type == pygame.MOUSEBUTTONUP:
        clicked = False

    if clicked is True:
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
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

    clock.tick(20)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

pygame.quit()
