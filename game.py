import math
import pygame
import numpy as np
import pygame.surfarray as surfarray

# crée une palette de couleurs
from math import sqrt
from pygame.transform import scale

pygame.init()

pygame.display.set_caption("Wargame")

palette = {
    'B': [0, 0, 255],
    ' ': [0, 0, 0],
    'W': [255, 255, 255],
    'G': [0, 255, 0],
    'R': [255, 0, 0],
    'Y': [255, 255, 0],
    'C': [0, 225, 255]
}  # initialise un dictionnaire

black = (0, 0, 0, 255)
blue = (0, 0, 255, 255)

WIDTH = 20  # largeur d'une case en pixels
NBcases = 20
screen_size = [WIDTH * NBcases, WIDTH * NBcases]
screen = pygame.display.set_mode(screen_size)
plan = ['GGGGGGGGGGGGGGGGGGGG',
        'BBBBBBBBBGGBBBBBBBBB',
        'BBBBBGGGGGGGGGGBBGGB',
        'BBBBBBBBBGGBBBBBBGGB',
        'BBGGBGGBBGGBBGGGGGGB',
        'BBBBBBGGBGGBBBGGGGGG',
        'BBBBBBBBBGGBBBGGBBBB',
        'GGBGGBGGBBBBBBGGBBGG',
        'BBBBBBBBBGGBBBBBBBGG',
        'GGBBGGGGGGBBBBGGGGGG',
        'GGBBGGBBBBBBGGBBBGGB',
        'GGBGGBBGGBBBBBGGBGGB',
        'GGBBBBBGGBGGBBBBBGGB',
        'GGGGGGGGBBBBBBGGGGGG',
        'BBBBBBBBBBGGGGGGGGGG',
        'GGBBBGGBBGGGGBBBBGGB',
        'GGBBBBBGGBBBBGGBBBBB',
        'GGBBGGBBGGGBBGGBBGGB',
        'GGBBBBBBBBBBBBBBBBGG',
        'GGGGGGGGGGGGGGGGGGGG']

# verification du plan

if len(plan) != NBcases: print("erreur, nombre de lignes dans le plan")
for ligne in plan:
    if len(ligne) != NBcases: print("erreur, ligne pas à la bonne dimension")

# remplissage du tableau du labyrinthe
LABY = np.zeros((NBcases, NBcases, 3))
for y in range(NBcases):
    ligne = plan[y]
    for x in range(NBcases):
        c = ligne[x]
        LABY[x, y] = palette[c]


def ToSprite(ascii) -> pygame.Surface:
    _larg = len(max(ascii, key=len))  # on prend la ligne la plus grande
    _haut = len(ascii)
    TBL = np.zeros((_larg, _haut, 3))  # tableau 3 dimensions

    for y in range(_haut):
        ligne = ascii[y]
        for x in range(len(ligne)):
            c = ligne[x]  # on recupere la lettre
            TBL[x, y] = palette[c]  # on stocke le code couleur RVB

    # conversion du tableau de RVB en sprite pygame
    sprite = surfarray.make_surface(TBL)
    return sprite


clock = pygame.time.Clock()

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    for ix in range(NBcases):
        for iy in range(NBcases):
            xpix = WIDTH * ix
            ypix = WIDTH * iy
            couleur = LABY[ix, iy]
            pygame.draw.rect(screen, couleur, [xpix, ypix, WIDTH, WIDTH])

    clock.tick(30)

    pygame.display.flip()

pygame.quit()
