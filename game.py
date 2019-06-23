import inspect
import os

import numpy as np
import pygame
from math import sqrt
from pygame import transform
from pygame.draw import rect
from pygame.font import SysFont
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.transform import scale

from classunite import ClasseUnite
from common import palette, RED, WHITE, YELLOW, BLACK, unite_assets, GREEN
from unite import Unite

scriptPATH = os.path.abspath(inspect.getsourcefile(lambda: 0))  # compatible interactive Python Shell
scriptDIR = os.path.dirname(scriptPATH)
assets = os.path.join(scriptDIR, "data/unites")

pygame.init()

pygame.display.set_caption("Wargame")

son = pygame.mixer.Sound(os.path.join(scriptDIR, "musique/hoi2-kriegsgewitter.wav"))
son.play(loops=-1)

police = pygame.font.SysFont("arial", 15, True)

base_hp = 100

taille_case = 40
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

bases = [
    {
        "X": 0,
        "Y": 0,
        "hp": base_hp,
    },
    {
        "X": 0,
        "Y": 0,
        "hp": base_hp,
    },
]

x_counter = 0
y_counter = 0
base_counter = 0
for line in plan:
    for letter in line:
        if letter == "B":
            bases[base_counter]["X"] = x_counter
            bases[base_counter]["Y"] = y_counter
            if base_counter > 1:
                raise Exception("Il ne peut y avoir que 2 bases par carte")
            base_counter += 1
        x_counter += 1
    x_counter = 0
    y_counter += 1

terrain_dim = [len(plan[0]), len(plan)]

WINDOW_SIZE = [taille_case * terrain_dim[0], taille_case * terrain_dim[1] + 1]
screen = pygame.display.set_mode(WINDOW_SIZE)

argent_player = [2000, 2000]
revenu = [1000, 1000]

clock = pygame.time.Clock()

units = {

    "infanterie": ClasseUnite("infanterie",
                              pygame.image.load(os.path.join(unite_assets, "0_inf.png")),
                              pygame.image.load(os.path.join(unite_assets, "1_inf.png")),
                              range(1, 1),
                              {
                                  "movepoint": 4,
                                  "cost": 500,
                                  "manpower": 10000,
                                  "supplies": 1,
                                  "defaultorga": 50,
                                  "defensiveness": 10,
                                  "toughness": 10,
                                  "softness": 90,
                                  "airdefence": 20,
                                  "softattack": 80,
                                  "hardattack": 10,
                                  "airattack": 10,
                                  "hp": 100
                              },
                              {
                                  'B': 1,  # base
                                  'E': 2,  # eau
                                  'R': 0.5,  # route
                                  'V': 1,  # ville
                                  'f': 1.5,  # foret
                                  'S': 1,  # plage
                                  'M': 4,  # montagne
                                  'C': 2,  # colline
                                  'P': 1,  # plaine
                                  'F': 1,  # fort
                                  'T': 1,  # recherche
                                  'U': 1,  # Usine M
                                  'u': 1,  # Usine C
                                  ' ': -1  # void
                              }),
    "infMontagne": ClasseUnite("infanterie de montagne",
                               pygame.image.load(os.path.join(unite_assets, "0_infM.png")),
                               pygame.image.load(os.path.join(unite_assets, "1_infM.png")),
                               range(1, 1),
                               {
                                   "movepoint": 4,
                                   "cost": 650,
                                   "manpower": 10000,
                                   "supplies": 1,
                                   "defaultorga": 50,
                                   "defensiveness": 15,
                                   "toughness": 10,
                                   "softness": 90,
                                   "airdefence": 20,
                                   "softattack": 80,
                                   "hardattack": 10,
                                   "airattack": 10,
                                   "hp": 100
                               },
                               {
                                   'B': 1,  # base
                                   'E': 2,  # eau
                                   'R': 0.5,  # route
                                   'V': 1,  # ville
                                   'f': 1.5,  # foret
                                   'S': 1,  # plage
                                   'M': 1.5,  # montagne
                                   'C': 1,  # colline
                                   'P': 1,  # plaine
                                   'F': 1,  # fort
                                   'T': 1,  # recherche
                                   'U': 1,  # Usine M
                                   'u': 1,  # Usine C
                                   ' ': -1  # void
                               }),
    "genie": ClasseUnite("génie",
                         pygame.image.load(os.path.join(unite_assets, "0_inge.png")),
                         pygame.image.load(os.path.join(unite_assets, "1_inge.png")),
                         range(1, 1),
                         {
                             "movepoint": 4,
                             "cost": 800,
                             "manpower": 10000,
                             "supplies": 1,
                             "defaultorga": 50,
                             "defensiveness": 10,
                             "toughness": 10,
                             "softness": 90,
                             "airdefence": 30,
                             "softattack": 60,
                             "hardattack": 30,
                             "airattack": 10,
                             "hp": 100
                         },
                         {
                             'B': 1,  # base
                             'E': 1.5,  # eau
                             'R': 0.5,  # route
                             'V': 1,  # ville
                             'f': 1.5,  # foret
                             'S': 1,  # plage
                             'M': 3,  # montagne
                             'C': 2,  # colline
                             'P': 1,  # plaine
                             'F': 1,  # fort
                             'T': 1,  # recherche
                             'U': 1,  # Usine M
                             'u': 1,  # Usine C
                             ' ': -1  # void
                         }),
    "SOP": ClasseUnite("SOP",
                       pygame.image.load(os.path.join(unite_assets, "0_Special_Operations_Forces.png")),
                       pygame.image.load(os.path.join(unite_assets, "1_Special_Operations_Force.png")),
                       range(1, 2),
                       {
                           "movepoint": 5,
                           "cost": 1200,
                           "manpower": 10000,
                           "supplies": 1,
                           "defaultorga": 50,
                           "defensiveness": 20,
                           "toughness": 10,
                           "softness": 90,
                           "airdefence": 20,
                           "softattack": 70,
                           "hardattack": 35,
                           "airattack": 10,
                           "hp": 100
                       },
                       {
                           'B': 1,  # base
                           'E': 1,  # eau
                           'R': 0.5,  # route
                           'V': 0.5,  # ville
                           'f': 1,  # foret
                           'S': 1,  # plage
                           'M': 2.5,  # montagne
                           'C': 1.5,  # colline
                           'P': 1,  # plaine
                           'F': 1,  # fort
                           'T': 1,  # recherche
                           'U': 1,  # Usine M
                           'u': 1,  # Usine C
                           ' ': -1  # void
                       }),
    "reco": ClasseUnite("reconnaissance",
                        pygame.image.load(os.path.join(unite_assets, "0_reco.png")),
                        pygame.image.load(os.path.join(unite_assets, "1_reco.png")),
                        range(1, 1),
                        {
                            "movepoint": 6,
                            "cost": 1000,
                            "manpower": 10000,
                            "supplies": 1,
                            "defaultorga": 50,
                            "defensiveness": 15,
                            "toughness": 25,
                            "softness": 50,
                            "airdefence": 20,
                            "softattack": 60,
                            "hardattack": 15,
                            "airattack": 10,
                            "hp": 100
                        },
                        {
                            'B': 1,  # base
                            'E': -1,  # eau
                            'R': 0.5,  # route
                            'V': 1,  # ville
                            'f': 1.5,  # foret
                            'S': 1,  # plage
                            'M': -1,  # montagne
                            'C': 1.5,  # colline
                            'P': 1,  # plaine
                            'F': 1,  # fort
                            'T': 1,  # recherche
                            'U': 1,  # Usine M
                            'u': 1,  # Usine C
                            ' ': 1  # void
                        }),
    "infMeca": ClasseUnite("infanterie mecaniser",
                           pygame.image.load(os.path.join(unite_assets, "0_infMeca.png")),
                           pygame.image.load(os.path.join(unite_assets, "1_infMeca.png")),
                           range(1, 1),
                           {
                               "movepoint": 6,
                               "cost": 1500,
                               "manpower": 10000,
                               "supplies": 1,
                               "defaultorga": 50,
                               "defensiveness": 30,
                               "toughness": 30,
                               "softness": 70,
                               "airdefence": 20,
                               "softattack": 90,
                               "hardattack": 30,
                               "airattack": 10,
                               "hp": 100
                           },
                           {
                               'B': 1,  # base
                               'E': -1,  # eau
                               'R': 0.5,  # route
                               'V': 1,  # ville
                               'f': 2,  # foret
                               'S': 1,  # plage
                               'M': -1,  # montagne
                               'C': 2,  # colline
                               'P': 1,  # plaine
                               'F': 1,  # fort
                               'T': 1,  # recherche
                               'U': 1,  # Usine M
                               'u': 1,  # Usine C
                               ' ': 1  # void
                           }),
    "mortier": ClasseUnite("mortier",
                           pygame.image.load(os.path.join(unite_assets, "0_mortier.png")),
                           pygame.image.load(os.path.join(unite_assets, "1_mortier.png")),
                           range(1, 2),
                           {
                               "movepoint": 4,
                               "cost": 500,
                               "manpower": 10000,
                               "supplies": 1,
                               "defaultorga": 50,
                               "defensiveness": 10,
                               "toughness": 10,
                               "softness": 90,
                               "airdefence": 20,
                               "softattack": 50,
                               "hardattack": 50,
                               "airattack": 1,
                               "hp": 100
                           },
                           {
                               'B': 1,  # base
                               'E': -1,  # eau
                               'R': 0.5,  # route
                               'V': 1,  # ville
                               'f': 1.5,  # foret
                               'S': 1,  # plage
                               'M': 4,  # montagne
                               'C': 2,  # colline
                               'P': 1,  # plaine
                               'F': 1,  # fort
                               'T': 1,  # recherche
                               'U': 1,  # Usine M
                               'u': 1,  # Usine C
                               ' ': -1  # void
                           }),
    "artillerie": ClasseUnite("artillerie",
                              pygame.image.load(os.path.join(unite_assets, "0_arty.png")),
                              pygame.image.load(os.path.join(unite_assets, "1_arty.png")),
                              range(2, 4),
                              {
                                  "movepoint": 3,
                                  "cost": 1000,
                                  "manpower": 10000,
                                  "supplies": 1,
                                  "defaultorga": 50,
                                  "defensiveness": 10,
                                  "toughness": 10,
                                  "softness": 90,
                                  "airdefence": 10,
                                  "softattack": 80,
                                  "hardattack": 80,
                                  "airattack": 10,
                                  "hp": 100
                              },
                              {
                                  'B': 1,  # base
                                  'E': -1,  # eau
                                  'R': 0.5,  # route
                                  'V': 1,  # ville
                                  'f': 2,  # foret
                                  'S': 1,  # plage
                                  'M': -1,  # montagne
                                  'C': 3,  # colline
                                  'P': 1,  # plaine
                                  'F': 1,  # fort
                                  'T': 1,  # recherche
                                  'U': 1,  # Usine M
                                  'u': 1,  # Usine C
                                  ' ': -1  # void
                              }),
    "AA": ClasseUnite("AA",
                      pygame.image.load(os.path.join(unite_assets, "0_AA.png")),
                      pygame.image.load(os.path.join(unite_assets, "1_AA.png")),
                      range(1, 1),
                      {
                          "movepoint": 6,
                          "cost": 1200,
                          "manpower": 10000,
                          "supplies": 1,
                          "defaultorga": 50,
                          "defensiveness": 10,
                          "toughness": 10,
                          "softness": 90,
                          "airdefence": 80,
                          "softattack": 95,
                          "hardattack": 5,
                          "airattack": 60,
                          "hp": 100
                      },
                      {
                          'B': 1,  # base
                          'E': -1,  # eau
                          'R': 0.5,  # route
                          'V': 1,  # ville
                          'f': 1.5,  # foret
                          'S': 1,  # plage
                          'M': -1,  # montagne
                          'C': 1.5,  # colline
                          'P': 1,  # plaine
                          'F': 1,  # fort
                          'T': 1,  # recherche
                          'U': 1,  # Usine M
                          'u': 1,  # Usine C
                          ' ': 1  # void
                      }),
    "MAA": ClasseUnite("missille AA",
                       pygame.image.load(os.path.join(unite_assets, "0_MAA.png")),
                       pygame.image.load(os.path.join(unite_assets, "1_MAA.png")),
                       range(2, 4),
                       {
                           "movepoint": 3,
                           "cost": 2000,
                           "manpower": 10000,
                           "supplies": 1,
                           "defaultorga": 50,
                           "defensiveness": 10,
                           "toughness": 30,
                           "softness": 70,
                           "airdefence": 95,
                           "softattack": 10,
                           "hardattack": 10,
                           "airattack": 95,
                           "hp": 100
                       },
                       {
                           'B': 1,  # base
                           'E': -1,  # eau
                           'R': 0.5,  # route
                           'V': 1,  # ville
                           'f': 2,  # foret
                           'S': 1,  # plage
                           'M': -1,  # montagne
                           'C': 3,  # colline
                           'P': 1,  # plaine
                           'F': 1,  # fort
                           'T': 1,  # recherche
                           'U': 1,  # Usine M
                           'u': 1,  # Usine C
                           ' ': -1  # void
                       }),
    "tank": ClasseUnite("tank",
                        pygame.image.load(os.path.join(unite_assets, "0_tank.png")),
                        pygame.image.load(os.path.join(unite_assets, "1_tank.png")),
                        range(1, 2),
                        {  # tintin's stat
                            "movepoint": 5,  # point de mouvement
                            "cost": 2500,  # argent requis lors du recrutement
                            "manpower": 10000,  # man power requis "		"
                            "supplies": 5,  # point de supplie "		"
                            "defaultorga": 50,  # multiplicateur globale de l'efficacité de l'unité [0-100]
                            "defensiveness": 50,  # stat défensive[0-100]
                            "toughness": 80,  # point de vie (Hard) (toughness+softness=100)
                            "softness": 20,  # point de vie (soft)
                            "airdefence": 10,  # stat défensive anti-aérien[0-100] (réduction des dégat subit)
                            "softattack": 20,  # stat attaque (Soft)
                            "hardattack": 80,  # stat attaque (Hard)
                            "airattack": 10,  # stat attaque anti-aérien (dégat infliger),
                            "hp": 100
                        },
                        {
                            'B': 1,  # base
                            'E': -1,  # eau
                            'R': 0.5,  # route
                            'V': 1,  # ville
                            'f': 2,  # foret
                            'S': 1,  # plage
                            'M': -1,  # montagne
                            'C': 2,  # colline
                            'P': 1,  # plaine
                            'F': 1,  # fort
                            'T': 1,  # recherche
                            'U': 1,  # Usine M
                            'u': 1,  # Usine C
                            ' ': 1  # void
                        }),
    "antiTank": ClasseUnite("anti-tank",
                            pygame.image.load(os.path.join(unite_assets, "0_antiTank.png")),
                            pygame.image.load(os.path.join(unite_assets, "1_anti_tank.png")),
                            range(1, 2),
                            {
                                "movepoint": 3,
                                "cost": 1000,
                                "manpower": 10000,
                                "supplies": 1,
                                "defaultorga": 50,
                                "defensiveness": 30,
                                "toughness": 75,
                                "softness": 25,
                                "airdefence": 20,
                                "softattack": 10,
                                "hardattack": 90,
                                "airattack": 10,
                                "hp": 100
                            },
                            {
                                'B': 1,  # base
                                'E': 2,  # eau
                                'R': 0.5,  # route
                                'V': 1,  # ville
                                'f': 1.5,  # foret
                                'S': 1,  # plage
                                'M': 4,  # montagne
                                'C': 2,  # colline
                                'P': 1,  # plaine
                                'F': 1,  # fort
                                'T': 1,  # recherche
                                'U': 1,  # Usine M
                                'u': 1,  # Usine C
                                ' ': -1  # void
                            }),
    "tankD": ClasseUnite("chasseur de char",
                         pygame.image.load(os.path.join(unite_assets, "0_tankD.png")),
                         pygame.image.load(os.path.join(unite_assets, "1_tankD.png")),
                         range(1, 1),
                         {
                             "movepoint": 5,
                             "cost": 2000,
                             "manpower": 10000,
                             "supplies": 1,
                             "defaultorga": 50,
                             "defensiveness": 40,
                             "toughness": 10,
                             "softness": 90,
                             "airdefence": 20,
                             "softattack": 10,
                             "hardattack": 80,
                             "airattack": 10,
                             "hp": 100
                         },
                         {
                             'B': 1,  # base
                             'E': -1,  # eau
                             'R': 0.5,  # route
                             'V': 1,  # ville
                             'f': 2,  # foret
                             'S': 1,  # plage
                             'M': -1,  # montagne
                             'C': 2,  # colline
                             'P': 1,  # plaine
                             'F': 1,  # fort
                             'T': 1,  # recherche
                             'U': 1,  # Usine M
                             'u': 1,  # Usine C
                             ' ': 1  # void
                         }),
    "chasseur": ClasseUnite("chasseur",
                            pygame.image.load(os.path.join(unite_assets, "0_fighter.png")),
                            pygame.image.load(os.path.join(unite_assets, "1_fighter.png")),
                            range(1, 1),
                            {
                                "movepoint": 10,
                                "cost": 2200,
                                "manpower": 10000,
                                "supplies": 1,
                                "defaultorga": 50,
                                "defensiveness": 20,
                                "toughness": 10,
                                "softness": 90,
                                "airdefence": 50,
                                "softattack": 20,
                                "hardattack": 5,
                                "airattack": 50,
                                "hp": 100
                            },
                            {
                                'B': 1,  # base
                                'E': 1,  # eau
                                'R': 1,  # route
                                'V': 1,  # ville
                                'f': 1,  # foret
                                'S': 1,  # plage
                                'M': 1,  # montagne
                                'C': 1,  # colline
                                'P': 1,  # plaine
                                'F': 1,  # fort
                                'T': 1,  # recherche
                                'U': 1,  # Usine M
                                'u': 1,  # Usine C
                                ' ': -1  # void
                            }),
    "bombardier": ClasseUnite("bombardier",
                              pygame.image.load(os.path.join(unite_assets, "0_bomber.png")),
                              pygame.image.load(os.path.join(unite_assets, "1_bomber.png")),
                              range(1, 1),
                              {
                                  "movepoint": 8,
                                  "cost": 4000,
                                  "manpower": 10000,
                                  "supplies": 1,
                                  "defaultorga": 50,
                                  "defensiveness": 30,
                                  "toughness": 10,
                                  "softness": 90,
                                  "airdefence": 20,
                                  "softattack": 60,
                                  "hardattack": 80,
                                  "airattack": 100,
                                  "hp": 100
                              },
                              {
                                  'B': 1,  # base
                                  'E': 1,  # eau
                                  'R': 1,  # route
                                  'V': 1,  # ville
                                  'f': 1,  # foret
                                  'S': 1,  # plage
                                  'M': 1,  # montagne
                                  'C': 1,  # colline
                                  'P': 1,  # plaine
                                  'F': 1,  # fort
                                  'T': 1,  # recherche
                                  'U': 1,  # Usine M
                                  'u': 1,  # Usine C
                                  ' ': -1  # void
                              }),
}
units_id = []

terrain_units = [
    Unite(WINDOW_SIZE[0], WINDOW_SIZE[1], 1, units["infanterie"]),
]
done = False

selected_unit = -1
selected_unit_create = -1
lastclick = False

tour_equipe = 0

terrain_bonus = {
    'B': 3,
    'E': 0.25,
    'R': 0.75,
    'V': 2,
    'f': 1.5,
    'S': 0.5,
    'M': 3,
    'C': 2,
    'P': 1,
    'F': 3,
    'T': 2,
    'U': 2,
    'u': 2,
    ' ': 1,
}


def equipe_differente(unite1: int, unite2: int) -> bool:
    return terrain_units[unite1].equipe != terrain_units[unite2].equipe


def attaque(id_unite: int, id_cible: int):
    print(str(id_unite) + " attaque " + str(id_cible))

    terrain_units[id_unite].att = True
    unite = terrain_units[id_unite]
    cible = terrain_units[id_cible]
    terrain_u = plan[unite.X][unite.Y]
    terrain_c = plan[cible.X][cible.Y]
    print(terrain_c)

    # Début de attaque
    cible.hp -= int(((unite.classeunite.stat["softattack"] / cible.classeunite.stat["softness"]) + (
            unite.classeunite.stat["hardattack"] / cible.classeunite.stat["toughness"]) + (
                             unite.classeunite.stat["airattack"] / cible.classeunite.stat["airdefence"])) * (
                            unite.classeunite.stat["hp"] / cible.classeunite.stat["defensiveness"] * (
                            1 / terrain_bonus[terrain_c])))
    # print(cible.hp)
    # print(terrain_var(terrain_c))
    if cible.hp <= 0:
        terrain_units.remove(cible)
        return

    # Fin de attaque
    terrain_units[id_unite] = unite
    terrain_units[id_cible] = cible


def attaque_range(id_unite: int, id_cible: int):
    if id_unite == id_cible:
        return False
    type = terrain_units[id_unite].classeunite
    min = float(type.cible.start)
    max = float(type.cible.stop)
    dist = distance(terrain_units[id_unite].X, terrain_units[id_unite].Y,
                    terrain_units[id_cible].X, terrain_units[id_cible].Y)
    return min <= dist <= max


def distance(x1, y1, x2, y2) -> float:
    return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))


def trans_case(color, pos):
    s = Surface((taille_case, taille_case))
    s.set_alpha(100)
    s.fill(color)
    screen.blit(s, (pos[0] * taille_case, pos[1] * taille_case))


def changer_tour():
    global tour_equipe
    global selected_unit
    print("TOUR SUIVANT")
    argent_player[tour_equipe] += revenu[tour_equipe]
    tour_equipe = 1 - tour_equipe
    selected_unit = -1
    for unite in terrain_units:
        if unite.equipe == tour_equipe:
            unite.nouveau_tour()


def verifier_touche():
    global taille_case
    global lastclick
    global done

    click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_handler()
            click = True
    if click is False:
        lastclick = False
    pygame.event.pump()

    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_PAGEUP]:
        taille_case += 1

    elif keys_pressed[pygame.K_PAGEDOWN]:
        taille_case -= 1


def click_handler():
    global lastclick
    global selected_unit
    global selected_unit_create
    global terrain
    global terrain_dim
    global units
    global bases

    if lastclick:
        return
    else:
        lastclick = True

    pos = pygame.mouse.get_pos()
    x_cursor = pos[0] // taille_case
    y_cursor = pos[1] // taille_case

    # Gestion de la barre d'outils
    if y_cursor >= terrain_dim[1]:
        # BTN tour suivant
        if terrain_dim[0] - 2 <= x_cursor <= terrain_dim[0] and terrain_dim[1] - 1 <= y_cursor <= terrain_dim[0]:
            changer_tour()
        # Création d'unite
        elif x_cursor == selected_unit_create:
            selected_unit_create = -1
        elif x_cursor < len(units_id):
            selected_unit_create = x_cursor
        return

    # Gestion du clique sur unité
    for unite in terrain_units:
        xu = unite.X * taille_case
        yu = unite.Y * taille_case

        # Detection de la collision (entre la souris et l'unité)
        rect_col = Rect(xu, yu, taille_case, taille_case)
        if rect_col.collidepoint(x_cursor * taille_case, y_cursor * taille_case):
            cible_id = terrain_units.index(unite)
            if cible_id != selected_unit:
                # Si une unité est déjà select
                if selected_unit != -1:
                    if equipe_differente(selected_unit, cible_id) and attaque_range(selected_unit, cible_id) \
                            and terrain_units[selected_unit].att is False:
                        attaque(selected_unit, cible_id)
                    selected_unit = -1
                elif terrain_units[cible_id].equipe == tour_equipe:
                    selected_unit = cible_id
            else:
                selected_unit = -1

            # S'il s'agissait d'une unité alors il ne sert à rien de rester dans la fonction
            return

    x_base_adv = bases[1 - tour_equipe]["X"]
    y_base_adv = bases[1 - tour_equipe]["Y"]
    sunit = terrain_units[selected_unit]
    distance_base = distance(sunit.X, sunit.Y, x_base_adv, y_base_adv)
    if x_base_adv == x_cursor and y_base_adv == y_cursor and selected_unit != -1 and sunit.att is False \
            and sunit.classeunite.cible.start <= distance_base <= sunit.classeunite.cible.stop:
        bases[1 - tour_equipe]["hp"] -= sunit.classeunite.stat["softattack"]
        sunit.att = True
        return

    # Si on ne clique pas sur une unité

    # Si une unité est sur le point d'être acheté
    x_base_all = bases[tour_equipe]["X"]
    y_base_all = bases[tour_equipe]["Y"]
    if selected_unit_create != -1 and distance(x_base_all, y_base_all, x_cursor, y_cursor) < 2:
        type_u = units[units_id[selected_unit_create]]
        cout = type_u.stat["cost"]

        if cout <= argent_player[tour_equipe]:
            argent_player[tour_equipe] -= cout
            terrain_units.append(
                Unite(int(x_cursor), int(y_cursor), tour_equipe, units[units_id[selected_unit_create]]))
        else:
            print("Pas assez d'argent pour acheter l'unité")

        selected_unit_create = -1
        return

    # Si une unité est select
    elif selected_unit != -1:
        unite = terrain_units[selected_unit]
        x_unit = unite.X
        y_unit = unite.Y
        terrain = plan[y_cursor][x_cursor]
        cout = unite.classeunite.terrain[terrain]
        dep = unite.pts_dep

        dist = distance(x_unit, y_unit, x_cursor, y_cursor)
        if dist == 1 and -1 != cout <= dep:
            terrain_units[selected_unit].deplacer(x_cursor, y_cursor, cout)
        return


def afficher_terrain():
    screen.fill(WHITE)
    laby = np.zeros((terrain_dim[0], terrain_dim[1]), pygame.Surface)
    for y in range(terrain_dim[1]):
        ligne = plan[y]
        ypix = taille_case * y
        for x in range(terrain_dim[0]):
            xpix = taille_case * x
            biome = ligne[x]
            image = transform.scale(palette['P'], (taille_case, taille_case))
            screen.blit(image, [xpix, ypix])
            image = transform.scale(palette[biome], (taille_case, taille_case))
            screen.blit(image, [xpix, ypix])

    trans_case(GREEN, (bases[0]["X"], bases[0]["Y"]))
    afficher_hp(bases[0]["hp"], bases[0]["X"], bases[0]["Y"])
    trans_case(RED, (bases[1]["X"], bases[1]["Y"]))
    afficher_hp(bases[1]["hp"], bases[1]["X"], bases[1]["Y"])


def afficher_unite():
    for unite in terrain_units:
        cible_id = terrain_units.index(unite)

        if selected_unit == cible_id:
            select_rect = Rect(unite.X * taille_case, unite.Y * taille_case, taille_case, taille_case)
            rect(screen, [255, 100, 0], select_rect)

        image: Surface
        if unite.equipe == 1:
            image = unite.classeunite.sprite2
        else:
            image = unite.classeunite.sprite1

        icon_unite: Surface = scale(image, (taille_case // 2, taille_case // 2))
        screen.blit(icon_unite, (int((unite.X + 1 / 4) * taille_case), int((unite.Y + 1 / 4) * taille_case)))

        # Affichage des HP
        afficher_hp(terrain_units[cible_id].hp, terrain_units[cible_id].X, terrain_units[cible_id].Y)


def afficher_hp(hp: int, x, y):
    hp_text = police.render("HP: " + str(hp), True, WHITE)
    hp_text_rat = hp_text.get_height() / hp_text.get_width()
    hp_text = scale(hp_text, (taille_case, int(taille_case * hp_text_rat)))

    hp_surface = Surface((taille_case, int(taille_case * hp_text_rat)))
    hp_surface.fill((0, 0, 0))
    hp_surface.set_alpha(100)

    hp_surface.blit(hp_text, (0, 0))
    screen.blit(hp_surface,
                (x * taille_case, y * taille_case))


while not done:
    units_id = []
    for unite in units:
        units_id.append(unite)

    verifier_touche()
    WINDOW_SIZE = [taille_case * terrain_dim[0], taille_case * (terrain_dim[1] + 1)]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    afficher_terrain()

    # Affichage des unités
    afficher_unite()

    # Affichage des indications
    if selected_unit is not -1:
        sct_unite = terrain_units[selected_unit]
        sct_type = sct_unite.classeunite
        x_sct = sct_unite.X
        y_sct = sct_unite.Y
        equipe_sct = sct_unite.equipe
        dep = sct_unite.pts_dep

        # Affichage des indications de déplacement
        for case_x in range(-1, 2):
            for case_y in range(-1, 2):
                try:
                    terrain = plan[y_sct + case_y][x_sct + case_x]
                    cout = sct_type.terrain[terrain]
                    if dep >= cout != -1 and case_y != case_x != -case_y:
                        trans_case([0, 0, 255], (x_sct + case_x, y_sct + case_y))
                except:
                    ""

        # Affichage des indications de destruction
        for unite in terrain_units:
            x_unit = unite.X
            y_unit = unite.Y
            equipe_unit = unite.equipe
            if attaque_range(selected_unit, terrain_units.index(unite)) \
                    and terrain_units[selected_unit].att is False:
                if equipe_unit == equipe_sct:
                    trans_case([255, 0, 0], (x_unit, y_unit))
                else:
                    trans_case([0, 255, 0], (x_unit, y_unit))

    # Affichage bouton TOUR SUIVANT
    btn_toursuiv = Surface((taille_case * 2, taille_case))
    btn_toursuiv.fill(YELLOW)
    text = police.render("TOUR SUIVANT", True, BLACK)
    text = transform.scale(text, (taille_case * 2, taille_case))
    btn_toursuiv.blit(text, (0, 0))
    screen.blit(btn_toursuiv, ((terrain_dim[0] - 2) * taille_case, terrain_dim[1] * taille_case))

    # AFFICHAGE DU TOUR
    color = GREEN
    if tour_equipe == 1:
        color = RED
    text = police.render("TOUR DE L'EQUIPE " + str(tour_equipe + 1), True, color)
    text = transform.scale(text, (taille_case * 4, taille_case))
    screen.blit(text, ((terrain_dim[0] - 4) // 2 * taille_case, 0))

    # AFFICHAGE DES INFORMATIONS UTILISATEURS
    messages = [
        {
            "texte": "argent : ",
            "contenu": argent_player
        },
        {
            "texte": "revenu : ",
            "contenu": revenu
        }
    ]

    message_counter = 0
    for message in messages:
        y = message_counter * 20
        redtxt = police.render(message["texte"] + str(message["contenu"][1]), True, RED)
        bluetxt = police.render(message["texte"] + str(message["contenu"][0]), True, GREEN)
        screen.blit(redtxt, (0, y))
        screen.blit(bluetxt, (screen.get_width() - redtxt.get_width(), y))

        message_counter += 1

    # Affichage de la barre d'achat
    for unite in range(0, len(units_id)):
        unite_src = units[units_id[unite]]
        sprite_unite: Surface = unite_src.sprite1
        if tour_equipe == 1:
            sprite_unite = unite_src.sprite2

        image_unite = scale(sprite_unite, (taille_case - 4, taille_case - 4))
        frame_unite = Surface((taille_case, taille_case))
        if unite == selected_unit_create:
            frame_unite.fill((255, 255, 0))
        else:
            frame_unite.fill(WHITE)
        frame_unite.blit(image_unite, (2, 2))
        screen.blit(frame_unite, (taille_case * unite, taille_case * terrain_dim[1]))

    for base in bases:
        if base["hp"] <= 0:
            winr = SysFont("arial", 50, True).render("EQUIPE " + str(1 + (1 - bases.index(base))) + " GAGNE", True,
                                                     YELLOW)
            w, h = winr.get_size()
            screen.blit(scale(winr, (WINDOW_SIZE[0], int(h / w * WINDOW_SIZE[1]))), (0, WINDOW_SIZE[1] // 2))
    clock.tick(30)

    pygame.display.flip()

pygame.quit()
