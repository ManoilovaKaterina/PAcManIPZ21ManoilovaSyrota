from GameInit import GameObject

class Wall(GameObject):
    def __init__(self, surf, x, y, initSize: int, initColor=(15, 100, 200)):
        super().__init__(surf, x * initSize, y * initSize, initSize, initColor)

class Cookie(GameObject):
    def __init__(self, surf, x, y):
        super().__init__(surf, x, y, 4, (255, 209, 102), True)

class Powerup(GameObject):
    def __init__(self, surf, x, y):
        super().__init__(surf, x, y, 8, (255, 255, 255), True)