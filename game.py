import numpy as np
import pygame
from pygame.draw import circle, rect
from pygame.rect import Rect

pygame.init()

pygame.display.set_caption("Wargame")

palette = {
    'B': [154, 14, 159],  # base
    'E': [100, 104, 236],  # eau
    'R': [0, 0, 0],  # route
    'V': [255, 0, 0],  # ville
    'f': [10, 77, 15],  # foret
    'S': [208, 182, 77],  # plage
    'M': [88, 64, 9],  # montagne
    'C': [175, 149, 88],  # colline
    'P': [66, 164, 36],  # plaine
    'F': [87, 30, 5],  # fort
    'T': [255, 255, 255],  # recherche
    'U': [255, 255, 255],  # Usine M
    'u': [255, 255, 255],  # Usine C
    ' ': [255, 255, 255]  # void
}  # initialise un dictionnaire

black = (0, 0, 0, 255)
blue = (0, 0, 255, 255)

case_size = 40
plan = [
    "PPPPPPPPPSEESPPPPRRR",
    "PfffPPPPPSEESPPPPRBR",
    "fffffffPFSEESFffVRRR",
    "fffRRRRRRRRRRRRRRRFP",
    "PPfRVfPPSEESPffPPRPP",
    "PPPRffPPSEESPPffPRPP",
    "PPPRPPCPSEESPfffVRfP",
    "PPVRPPCPSEESPffffRfP",
    "PPPRPCCCSEESPPfffRPP",
    "PPPRPCCPSEESPPPPPRPP",
    "PPPRPCCPSEESMMPCCRVP",
    "PPFRVPPPSEEMMMPCCRPP",
    "RRRRPPPPSMMMMPPCPRPP",
    "RBRPPPPPMMMMPPPPRRPP",
    "RRRPPPPMMMMPPPPPPPPP",
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
        "Y": 2,
        "deplacement": 10
    },
    {
        "type": "tank",
        "X": 6,
        "Y": 4,
        "deplacement": 10
    },
    {
        "type": "tank",
        "X": 20,
        "Y": 8,
        "deplacement": 10
    },
    {
        "type": "tank",
        "X": 0,
        "Y": 0,
        "deplacement": 10
    },
    {
        "type": "fusilier",
        "X": 25,
        "Y": 10,
        "deplacement": 10
    },
]
done = False

selected_unit = -1

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

    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        for unite in terrain_units:
            xu = unite["X"] * case_size
            yu = unite["Y"] * case_size
            rectcol = Rect(xu, yu, case_size, case_size)
            if rectcol.collidepoint(x, y):
                selected_unit = terrain_units.index(unite)
        print()

    # Affichage des unités
    for unite in terrain_units:
        id = terrain_units.index(unite)
        if selected_unit == id:
            tank = Rect(unite["X"] * case_size, unite["Y"] * case_size, case_size, case_size)
            rect(screen, [255, 100, 0], tank)

        if unite["type"] == "fusilier":
            circle(screen, [255, 0, 255], (int((unite["X"] + 0.5) * case_size), int((unite["Y"] + 0.5) * case_size)),
                   20)
        elif unite["type"] == "tank":
            tank = Rect((unite["X"] * case_size) + case_size // 4, (unite["Y"] * case_size) + case_size // 4, case_size // 2, case_size // 2)
            rect(screen, [255, 255, 0], tank)
    clock.tick(30)

    pygame.display.flip()

pygame.quit()
