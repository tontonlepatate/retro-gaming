import inspect
import os

import numpy as np
import pygame
from math import sqrt
from pygame import transform
from pygame.draw import circle, rect
from pygame.rect import Rect
from pygame.surface import Surface

scriptPATH = os.path.abspath(inspect.getsourcefile(lambda: 0))  # compatible interactive Python Shell
scriptDIR = os.path.dirname(scriptPATH)
assets = os.path.join(scriptDIR, "data")

pygame.init()

pygame.display.set_caption("Wargame")

police = pygame.font.SysFont("arial", 15, True)

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]
RED = [255, 0, 0]
BLUE = [0, 0, 255]
YELLOW = [241, 244, 66]

image1_sprites = pygame.image.load(os.path.join(assets, "World_A1.png"))
image2_sprites = pygame.image.load(os.path.join(assets, "World_A2.png"))
image3_sprites = pygame.image.load(os.path.join(assets, "World_B.png"))
image4_sprites = pygame.image.load(os.path.join(assets, "World_C.png"))


def charger_sprite(feuille, x, y, size):
    planche_sprites = feuille
    planche_sprites.set_colorkey((0, 0, 0))
    return planche_sprites.subsurface((x, y, size, size))


palette = {
    'B': charger_sprite(image3_sprites, 383, 0, 95),  # base
    'E': charger_sprite(image1_sprites, 23, 70, 50),  # eau
    'R': charger_sprite(image2_sprites, 13, 210, 50),  # route
    'V': charger_sprite(image4_sprites, 0, 334, 95),  # ville
    'f': charger_sprite(image2_sprites, 385, 48, 95),  # foret
    'S': charger_sprite(image2_sprites, 22, 355, 48),  # plage
    'M': charger_sprite(image2_sprites, 671, 47, 95),  # montagne
    'C': charger_sprite(image2_sprites, 576, 47, 95),  # colline
    'P': charger_sprite(image2_sprites, 211, 70, 50),  # plaine
    'F': charger_sprite(image3_sprites, 673, 100, 95),  # fort
    'T': charger_sprite(image4_sprites, 470, 188, 95),  # recherche
    'U': charger_sprite(image4_sprites, 376, 188, 95),  # Usine M
    'u': charger_sprite(image4_sprites, 376, 282, 95),  # Usine C
    ' ': charger_sprite(image1_sprites, 364, 47, 47)  # void
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

WINDOW_SIZE = [case_size * terrain_dim[0], case_size * terrain_dim[1] + 1]
screen = pygame.display.set_mode(WINDOW_SIZE)

argent_player = [500, 500]
ptsrecherche = [10, 10]
supply = [10, 10]
impots = [10, 10]

clock = pygame.time.Clock()

units = {
    "tank": {
        "sprite": pygame.Surface((1, 1)),
        "terrains": {
            'B': 1,  # base
            'E': -1,  # eau
            'R': 1,  # route
            'V': -1,  # ville
            'f': 2,  # foret
            'S': 2,  # plage
            'M': -1,  # montagne
            'C': 2,  # colline
            'P': 1,  # plaine
            'F': -1,  # fort
            'T': -1,  # recherche
            'U': -1,  # Usine M
            'u': -1,  # Usine C
            ' ': -1  # void
        },
        "cible": {
            "min": 1,
            "max": 4
        },
        "stat": {  # tintin's stat
            "movepoint": 8,  # point de mouvement
            "cost": 10000,  # argent requis lors du recrutement
            "manpower": 10000,  # man power requis "		"
            "supplies": 5,  # point de supplie "		"
            "defaultorga": 50,  # multiplicateur globale de l'efficacité de l'unité [0-100]
            "defensiveness": 50,  # stat défensive[0-100]
            "toughness": 80,  # point de vie (Hard) (toughness+softness=100)
            "softness": 20,  # point de vie (soft)
            "airdefence": 10,  # stat défensive anti-aérien[0-100] (réduction des dégat subit)
            "softattack": 20,  # stat attaque (Soft)
            "hardattack": 80,  # stat attaque (Hard)
            "airattack": 10  # stat attaque anti-aérien (dégat infliger)
        },
    },

    "fusilier": {
        "sprite": pygame.Surface((1, 1)),
        "terrains": {
            'B': 1,  # base
            'E': 1,  # eau
            'R': 1,  # route
            'V': -1,  # ville
            'f': 3,  # foret
            'S': 3,  # plage
            'M': -1,  # montagne
            'C': 2,  # colline
            'P': 1,  # plaine
            'F': 1,  # fort
            'T': 1,  # recherche
            'U': 1,  # Usine M
            'u': 1,  # Usine C
            ' ': -1  # void
        },
        "cible": {
            "min": 0,
            "max": 3
        },
        "stat": {  # tintin's stat
            "movepoint": 4,
            "cost": 1000,
            "manpower": 10000,
            "supplies": 1,
            "defaultorga": 50,
            "defensiveness": 10,
            "toughness": 10,
            "softness": 90,
            "airdefence": 20,
            "softattack": 80,
            "hardattack": 10,
            "airattack": 10
        },
    },
}

terrain_units = [
    {
        "type": "fusilier",
        "X": 5,
        "Y": 2,
        "att": False,
        "hp": 10,
        "deplacement": 10,
        "equipe": 1
    },
    {
        "type": "tank",
        "X": 6,
        "Y": 4,
        "att": False,
        "hp": 10,
        "deplacement": 10,
        "equipe": 0
    },
    {
        "type": "tank",
        "X": 12,
        "Y": 8,
        "att": False,
        "deplacement": 10,
        "hp": 10,
        "equipe": 0
    },
    {
        "type": "tank",
        "X": 0,
        "Y": 0,
        "att": False,
        "hp": 10,
        "deplacement": 10,
        "equipe": 0
    },
    {
        "type": "fusilier",
        "X": 10,
        "Y": 10,
        "att": False,
        "hp": 10,
        "deplacement": 10,
        "equipe": 0
    },
]
done = False

selected_unit = -1
lastclick = False

tour_equipe = 0


def equipe_differente(unite1: int, unite2: int) -> bool:
    return terrain_units[unite1]["equipe"] != terrain_units[unite2]["equipe"]


def attaque(id_unite: int, id_cible: int):
    terrain_units[id_unite]["att"] = True
    unite = terrain_units[id_unite]
    cible = terrain_units[id_cible]
    # Début de attaque

    # Fin de attaque
    terrain_units[id_unite] = unite
    terrain_units[id_cible] = cible
    print(str(id_unite) + " attaque " + str(id_cible))


def attaque_range(id_unite: int, id_cible: int):
    if id_unite == id_cible:
        return False
    type = units[terrain_units[id_unite]["type"]]
    min = float(type["cible"]["min"])
    max = float(type["cible"]["max"])
    dist = distance(terrain_units[id_unite]["X"], terrain_units[id_unite]["Y"],
                    terrain_units[id_cible]["X"], terrain_units[id_cible]["Y"])
    return min <= dist <= max


def distance(x1, y1, x2, y2) -> float:
    return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))


def trans_case(color, pos):
    s = Surface((case_size, case_size))
    s.set_alpha(100)
    s.fill(color)
    screen.blit(s, (pos[0] * case_size, pos[1] * case_size))


def deplacement(id_unite):
    unite = terrain_units[id_unite]

    terrain_units[id_unite] = unite


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pygame.event.pump()

    KeysPressed = pygame.key.get_pressed()
    if KeysPressed[pygame.K_PAGEUP]:
        case_size += 1

    elif KeysPressed[pygame.K_PAGEDOWN]:
        case_size -= 1

    WINDOW_SIZE = [case_size * terrain_dim[0], case_size * (terrain_dim[1] + 1)]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    LABY = np.zeros((terrain_dim[0], terrain_dim[1]), pygame.Surface)
    for y in range(terrain_dim[1]):
        ligne = plan[y]
        for x in range(terrain_dim[0]):
            c = ligne[x]
            LABY[x, y] = palette[c]

    for ix in range(terrain_dim[0]):
        for iy in range(terrain_dim[1]):
            xpix = case_size * ix
            ypix = case_size * iy
            p = LABY[ix, iy]
            image = transform.scale(palette['P'], (case_size, case_size))
            screen.blit(image, [xpix, ypix])
            image = transform.scale(p, (case_size, case_size))
            screen.blit(image, [xpix, ypix])

    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        x = pos[0] // case_size
        y = pos[1] // case_size
        cible_unite = False
        if y >= terrain_dim[1]:
            if terrain_dim[0] - 2 <= x <= terrain_dim[0] and terrain_dim[1] - 1 <= y <= terrain_dim[0]:
                print("TOUR SUIVANT")
                argent_player[tour_equipe] += impots[tour_equipe]
                tour_equipe = 1 - tour_equipe
                selected_unit = -1
                for unite in terrain_units:
                    if unite["equipe"] == tour_equipe:
                        unite["att"] = False
                        unite["deplacement"] = 10

            cible_unite = True
        elif lastclick is not True:
            lastclick = True
            for unite in terrain_units:
                xu = unite["X"] * case_size
                yu = unite["Y"] * case_size
                rectcol = Rect(xu, yu, case_size, case_size)
                cible_id = terrain_units.index(unite)

                if rectcol.collidepoint(x * case_size, y * case_size):
                    cible_unite = True
                    if cible_id != selected_unit:
                        if selected_unit != -1:
                            if equipe_differente(selected_unit, cible_id) and attaque_range(selected_unit, cible_id) \
                                    and terrain_units[selected_unit]["att"] is False:
                                attaque(selected_unit, cible_id)
                            selected_unit = -1
                        elif terrain_units[cible_id]["equipe"] == tour_equipe:
                            selected_unit = cible_id
                    else:
                        selected_unit = -1
        if (cible_unite is False) and (selected_unit != -1):
            unite = terrain_units[selected_unit]
            x_unit = unite["X"]
            y_unit = unite["Y"]
            type_unit = units[unite["type"]]
            terrain = plan[y][x]
            cout = type_unit["terrains"][terrain]
            dep = unite["deplacement"]

            dist = distance(x_unit, y_unit, x, y)
            if dist == 1 and -1 != cout <= dep:
                terrain_units[selected_unit]["X"] = x
                terrain_units[selected_unit]["Y"] = y
                terrain_units[selected_unit]["deplacement"] -= cout
    else:
        lastclick = False

    # Affichage des unités
    for unite in terrain_units:
        cible_id = terrain_units.index(unite)
        if selected_unit == cible_id:
            select_rect = Rect(unite["X"] * case_size, unite["Y"] * case_size, case_size, case_size)
            rect(screen, [255, 100, 0], select_rect)

        if unite["type"] == "fusilier":
            circle(screen, [255, 0, 255], (int((unite["X"] + 0.5) * case_size), int((unite["Y"] + 0.5) * case_size)),
                   20)
        elif unite["type"] == "tank":
            tank = Rect((unite["X"] * case_size) + case_size // 4, (unite["Y"] * case_size) + case_size // 4,
                        case_size // 2, case_size // 2)
            rect(screen, [255, 255, 0], tank)

    if selected_unit is not -1:
        pos = pygame.mouse.get_pos()
        x = pos[0] // case_size
        y = pos[1] // case_size

        sct_unite = terrain_units[selected_unit]
        sct_type = units[sct_unite["type"]]
        x_sct = sct_unite["X"]
        y_sct = sct_unite["Y"]
        equipe_sct = sct_unite["equipe"]
        dep = sct_unite["deplacement"]

        for case_x in range(-1, 2):
            for case_y in range(-1, 2):
                terrain = plan[y_sct + case_y][x_sct + case_x]
                cout = sct_type["terrains"][terrain]
                if dep >= cout != -1 and case_y != case_x != -case_y:
                    trans_case([0, 0, 255], (x_sct + case_x, y_sct + case_y))

        for unite in terrain_units:
            x_unit = unite["X"]
            y_unit = unite["Y"]
            equipe_unit = unite["equipe"]
            if attaque_range(selected_unit, terrain_units.index(unite)) \
                    and terrain_units[selected_unit]["att"] is False:
                if equipe_unit == equipe_sct:
                    trans_case([255, 0, 0], (x_unit, y_unit))
                else:
                    trans_case([0, 255, 0], (x_unit, y_unit))

    # BOUTON TOUR SUIVANT
    btn_toursuiv = Surface((case_size * 2, case_size))
    btn_toursuiv.fill(YELLOW)
    text = police.render("TOUR SUIVANT", True, BLACK)
    text = transform.scale(text, (case_size * 2, case_size))
    btn_toursuiv.blit(text, (0, 0))
    screen.blit(btn_toursuiv, ((terrain_dim[0] - 2) * case_size, terrain_dim[1] * case_size))



    # AFFICHAGE DU TOUR
    color = BLUE
    if tour_equipe == 1:
        color = RED
    text = police.render("TOUR DE L'EQUIPE " + str(tour_equipe + 1), True, color)
    text = transform.scale(text, (case_size * 4, case_size))
    screen.blit(text, ((terrain_dim[0] - 4) // 2 * case_size, 0))

    # AFFICHAGE DES INFOS JOUEUR
    items = ["argent : ", "impots : ", "pts de recherche : ", "supply : ",
             "argent : ", "impots : ", "pts de recherche : ", "supply : "]
    variables = [argent_player[0], impots[0], ptsrecherche[0], supply[0], argent_player[1], impots[1], ptsrecherche[1],
                 supply[1]]
    colors = [BLUE, BLUE, BLUE, BLUE, RED, RED, RED, RED]
    coordonnées = [(0, 10), (0, 30), (0, 50), (0, 70), (case_size * terrain_dim[0] - 200, 10),
                   (case_size * terrain_dim[0] - 200, 30), (case_size * terrain_dim[0] - 200, 50),
                   (case_size * terrain_dim[0] - 200, 70)]

    for i, v, c, co in zip(items, variables, colors, coordonnées):
        text = police.render(i + str(v), True, c)
        screen.blit(text, co)

    clock.tick(30)

    pygame.display.flip()

pygame.quit()
