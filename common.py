import inspect
import os

import pygame

from classunite import ClasseUnite


def charger_sprite(feuille, x, y, size):
    planche_sprites = feuille
    planche_sprites.set_colorkey((0, 0, 0))
    return planche_sprites.subsurface((x, y, size, size))


scriptPATH = os.path.abspath(inspect.getsourcefile(lambda: 0))  # compatible interactive Python Shell
scriptDIR = os.path.dirname(scriptPATH)
assets = os.path.join(scriptDIR, "data")
unite_assets = os.path.join(assets, "unites")

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [170, 255, 170]
RED = [255, 50, 50]
BLUE = [0, 0, 255]
YELLOW = [241, 244, 66]

image1_sprites = pygame.image.load(os.path.join(assets, "World_A1.png"))
image2_sprites = pygame.image.load(os.path.join(assets, "World_A2.png"))
image3_sprites = pygame.image.load(os.path.join(assets, "World_B.png"))
image4_sprites = pygame.image.load(os.path.join(assets, "World_C.png"))

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
    ' ': charger_sprite(image2_sprites, 211, 70, 50),  # void
}  # initialise un dictionnaire

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
                       pygame.image.load(os.path.join(unite_assets, "0_SOP.png")),
                       pygame.image.load(os.path.join(unite_assets, "1_SOP.png")),
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
