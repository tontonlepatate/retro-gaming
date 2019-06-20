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
from common import palette, BLUE, RED, WHITE, YELLOW, BLACK, scriptDIR
from unite import Unite

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

argent_player = [500, 500]
ptsrecherche = [10, 10]
supply = [10, 10]
impots = [10, 10]

clock = pygame.time.Clock()

care_vert = pygame.Surface((1, 1))
care_vert.fill((0, 255, 0))

care_bleu = pygame.Surface((1, 1))
care_bleu.fill((0, 0, 255))

units = {
    "tank": ClasseUnite("tank", care_bleu, range(1, 4),
                        {  # tintin's stat
                            "movepoint": 8,  # point de mouvement
                            "cost": 1000,  # argent requis lors du recrutement
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
                        }),
    "fusilier": ClasseUnite("fusilier", care_vert, range(0, 3),
                            {
                                "movepoint": 4,
                                "cost": 100,
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
                                "hp": 10
                            },
                            {
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
                            })
}

units_id = []

terrain_units = [
    Unite(WINDOW_SIZE[0], WINDOW_SIZE[1], 1, units["fusilier"]),
]
done = False

selected_unit = -1
selected_unit_create = -1
lastclick = False

tour_equipe = 0


def equipe_differente(unite1: int, unite2: int) -> bool:
    return terrain_units[unite1].equipe != terrain_units[unite2].equipe


def attaque(id_unite: int, id_cible: int):
    print(str(id_unite) + " attaque " + str(id_cible))
    terrain_units[id_unite].att = True
    unite = terrain_units[id_unite]
    cible = terrain_units[id_cible]
    # Début de attaque
    cible.hp -= 10
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
    argent_player[tour_equipe] += impots[tour_equipe]
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
    laby = np.zeros((terrain_dim[0], terrain_dim[1]), pygame.Surface)
    for y in range(terrain_dim[1]):
        ligne = plan[y]
        for x in range(terrain_dim[0]):
            c = ligne[x]
            laby[x, y] = palette[c]

    for ix in range(terrain_dim[0]):
        for iy in range(terrain_dim[1]):
            xpix = taille_case * ix
            ypix = taille_case * iy
            p = laby[ix, iy]
            image = transform.scale(palette['P'], (taille_case, taille_case))
            screen.blit(image, [xpix, ypix])
            image = transform.scale(p, (taille_case, taille_case))
            screen.blit(image, [xpix, ypix])

    trans_case(BLUE, (bases[0]["X"], bases[0]["Y"]))
    afficher_hp(bases[0]["hp"], bases[0]["X"], bases[0]["Y"])
    trans_case(RED, (bases[1]["X"], bases[1]["Y"]))
    afficher_hp(bases[1]["hp"], bases[1]["X"], bases[1]["Y"])


def afficher_unite():
    for unite in terrain_units:
        cible_id = terrain_units.index(unite)

        if selected_unit == cible_id:
            select_rect = Rect(unite.X * taille_case, unite.Y * taille_case, taille_case, taille_case)
            rect(screen, [255, 100, 0], select_rect)

        icon_unite = scale(unite.classeunite.sprite, (taille_case // 2, taille_case // 2))
        filtre_equipe = Surface((icon_unite.get_width(), icon_unite.get_height()))
        filtre_equipe.set_alpha(100)
        if unite.equipe == 1:
            filtre_equipe.fill(BLUE)
        else:
            filtre_equipe.fill(RED)
        icon_unite.blit(filtre_equipe, (0, 0))
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
    color = BLUE
    if tour_equipe == 1:
        color = RED
    text = police.render("TOUR DE L'EQUIPE " + str(tour_equipe + 1), True, color)
    text = transform.scale(text, (taille_case * 4, taille_case))
    screen.blit(text, ((terrain_dim[0] - 4) // 2 * taille_case, 0))

    # AFFICHAGE DES INFOS JOUEUR
    items = ["argent : ", "impots : ", "pts de recherche : ", "supply : ",
             "argent : ", "impots : ", "pts de recherche : ", "supply : "]
    variables = [argent_player[0], impots[0], ptsrecherche[0], supply[0], argent_player[1], impots[1], ptsrecherche[1],
                 supply[1]]
    colors = [BLUE, BLUE, BLUE, BLUE, RED, RED, RED, RED]
    coordonnees = [(0, 10), (0, 30), (0, 50), (0, 70), (taille_case * terrain_dim[0] - 200, 10),
                   (taille_case * terrain_dim[0] - 200, 30), (taille_case * terrain_dim[0] - 200, 50),
                   (taille_case * terrain_dim[0] - 200, 70)]

    for i, v, c, co in zip(items, variables, colors, coordonnees):
        text = police.render(i + str(v), True, c)
        screen.blit(text, co)

    for unite in range(0, len(units_id)):
        unite_src = units[units_id[unite]]
        image_unite = scale(unite_src.sprite, (taille_case - 4, taille_case - 4))
        frame_unite = Surface((taille_case, taille_case))
        if unite == selected_unit_create:
            frame_unite.fill((255, 255, 0))
        else:
            frame_unite.fill((0, 0, 0))
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
