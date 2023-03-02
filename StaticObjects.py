from GameInit import GameObject

class Wall(GameObject):
    def __init__(self, surf, x, y, initSize: int, initColor=(15, 100, 200)):
        super().__init__(surf, x * initSize, y * initSize, initSize, initColor)
