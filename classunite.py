from pygame.surface import Surface


class ClasseUnite:
    nom: str
    sprite1: Surface
    sprite2: Surface
    cible: range
    stat: dict = {}
    terrain: dict = {}

    def __init__(self, _nom: str, _sprite1: Surface, _sprite2: Surface, _cible: range, _stat: dict, _terrain: dict):
        self.sprite1 = _sprite1
        self.sprite2 = _sprite2
        self.cible = _cible
        self.stat = _stat
        self.nom = _nom
        self.terrain = _terrain
