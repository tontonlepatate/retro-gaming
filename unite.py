from classunite import ClasseUnite


class Unite:
    X: int
    Y: int
    hp: int
    pts_dep: int
    att: bool
    equipe: int
    classeunite: ClasseUnite

    def __init__(self, _x: int, _y: int, _equipe: int, _type: ClasseUnite):
        self.classeunite = _type
        self.equipe = _equipe
        self.set_position(_x, _y)
        self.hp = self.classeunite.stat["hp"]
        self.nouveau_tour()

    def nouveau_tour(self):
        self.pts_dep = self.classeunite.stat["movepoint"]
        self.att = False

    def set_position(self, x: int, y: int):
        self.X = x
        self.Y = y

    def get_X(self) -> int:
        return self.X

    def get_Y(self) -> int:
        return self.Y

    def hit(self, degat: int):
        self.hp -= degat

    def a_attaque(self) -> bool:
        return self.att

    def deplacer(self, x: int, y: int, cout: int) -> bool:
        if cout <= self.pts_dep:
            self.set_position(x, y)
            self.pts_dep -= cout
            return True
        return False
