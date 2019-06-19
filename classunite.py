from pygame.surface import Surface


class ClasseUnite:
    nom: str
    sprite: Surface
    cible: range
    stat: dict = {}
    terrain: dict = {}

    def __init__(self, _nom: str, _sprite: Surface, _cible: range, _stat: dict, _terrain: dict):
        self.sprite = _sprite
        self.cible = _cible
        self.stat = _stat
        self.nom = _nom
        self.terrain = _terrain
