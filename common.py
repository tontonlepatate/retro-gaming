import inspect
import os

import pygame


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
GREEN = [0, 255, 0]
RED = [255, 0, 0]
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
