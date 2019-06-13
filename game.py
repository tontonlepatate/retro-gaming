import math
import pygame
import numpy as np
import pygame.surfarray as surfarray

# crée une palette de couleurs
from math import sqrt
from pygame.draw import circle, rect
from pygame.rect import Rect
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

case_size = 60
plan = [
    "WRBW BBBB  RBYBYW YR  BRY RWBB",
    "WYGBYGR BY GBGBRR YRWRWRRWBB B",
    "BWRGBB GWBRRRWGGGBRGBBWGBGBGRB",
    "WGGBWGWWRRGBYWBRBGRYBRY G WWY ",
    "GBWWGWRRRWYGBBYWYGRBRBY RRWGBR",
    "RGR WRRW BWGR  GGRGG GYRYB BWR",
    "WG BYBRY WG YBGB BWWYGW WBR W ",
    "BRWBRRYWWBB YW BWWGBRG BYGWW W",
    " YYY   GRY WYGBYGBGGGYWYYRBGYW",
    "WWWYBBGYYRWBG G GGYBWRWWRRGGGR",
    "GBYGR WY RRGGGGRRRYWWRWYGRRB B",
    " WG RW R BGY R  W RWW BYRRRY  ",
    "BYWRYGBY  GY YGGWRYYYRWWBBY YR",
    "GGBB GGGG BGYBRG GRGWWBRGYRWWB",
    "GYYYGBY YRYWWWR GYRBGBBY BWGRW",
]

terrain_dim = [len(plan[0]), len(plan)]

WINDOW_SIZE = [case_size * terrain_dim[0], case_size * terrain_dim[1]]
screen = pygame.display.set_mode(WINDOW_SIZE)

clock = pygame.time.Clock()

units = {
    "tank": {
        "sprite": pygame.Surface((1, 1)),
        "terrains": {
            "R": 1,
            "V": 2
        },
        "cible": {
            "min": 1,
            "max": 4
        }
    },

    "fusilier": {
        "sprite": pygame.Surface((1, 1)),
        "terrains": {
            "R": 10,
            "V": 10
        },
        "cible": {
            "min": 0,
            "max": 2
        }
    },
}

terrain_units = [
    {
        "type": "fusilier",
        "X": 5,
        "Y": 2
    },
    {
        "type": "tank",
        "X": 6,
        "Y": 4
    },
    {
        "type": "tank",
        "X": 20,
        "Y": 8
    },
{
        "type": "fusilier",
        "X": 25,
        "Y": 15
    },
]
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    LABY = np.zeros((terrain_dim[0], terrain_dim[1], 3))
    for y in range(terrain_dim[1]):
        ligne = plan[y]
        for x in range(terrain_dim[0]):
            c = ligne[x]
            LABY[x, y] = palette[c]

    for ix in range(terrain_dim[0]):
        for iy in range(terrain_dim[1]):
            xpix = case_size * ix
            ypix = case_size * iy
            couleur = LABY[ix, iy]
            pygame.draw.rect(screen, couleur, [xpix, ypix, case_size, case_size])

    # Affichage des unités
    for unite in terrain_units:
        if unite["type"] == "fusilier":
            circle(screen, [255, 0, 0], (int((unite["X"] - 0.5) * case_size), int((unite["Y"] - 0.5) * case_size)), 20)
        if unite["type"] == "tank":
            rect(screen, [255, 255, 0], Rect((unite["X"] * case_size) + 10, (unite["Y"] * case_size) + 10, 40, 40))
    clock.tick(30)

    pygame.display.flip()

pygame.quit()
