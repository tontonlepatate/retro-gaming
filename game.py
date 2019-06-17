import numpy as np
import pygame
from math import sqrt
from pygame.draw import circle, rect
from pygame.rect import Rect
from pygame.surface import Surface

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
        "deplacement": 10,
        "equipe": 1
    },
    {
        "type": "tank",
        "X": 6,
        "Y": 4,
        "deplacement": 10,
        "equipe": 0
    },
    {
        "type": "tank",
        "X": 12,
        "Y": 8,
        "deplacement": 10,
        "equipe": 0
    },
    {
        "type": "tank",
        "X": 0,
        "Y": 0,
        "deplacement": 10,
        "equipe": 0
    },
    {
        "type": "fusilier",
        "X": 10,
        "Y": 10,
        "deplacement": 10,
        "equipe": 0
    },
]
done = False

selected_unit = -1
lastclick = False


def equipe_differente(unite1: int, unite2: int) -> bool:
    return terrain_units[unite1] != terrain_units[unite2]["equipe"]


def attaque(id_unite: int, id_cible: int):
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


def distance(x1, y1, x2, y2):
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
        x = pos[0] // case_size
        y = pos[1] // case_size
        cible_unite = False
        if lastclick is not True:
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
                            if equipe_differente(selected_unit, cible_id) and attaque_range(selected_unit, cible_id):
                                attaque(selected_unit, cible_id)
                            selected_unit = -1
                        else:
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

            dist = int(distance(x_unit, y_unit, x, y))
            if dist == 1 and cout != -1 and cout <= dep:
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

        for unite in terrain_units:
            x_unit = unite["X"]
            y_unit = unite["Y"]
            equipe_unit = unite["equipe"]
            if attaque_range(selected_unit, terrain_units.index(unite)):
                if equipe_unit == equipe_sct:
                    trans_case([255, 0, 0], (x_unit, y_unit))
                else:
                    trans_case([0, 255, 0], (x_unit, y_unit))
    clock.tick(30)

    pygame.display.flip()

pygame.quit()
