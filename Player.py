import pygame

from GameInit import Direction
from MoveObj import MovableObject

class Player(MovableObject):
    def __init__(self, surf, x, y, initSize: int):
        super().__init__(surf, x, y, initSize, (255, 255, 0))
        self.lastNonCollidingPos = (0, 0)
        self.open = pygame.image.load("E:/UNI/2 курс/2 семестр/NI_RPZ/PacMan1.png")
        self.closed = pygame.image.load("E:/UNI/2 курс/2 семестр/NI_RPZ/PacMan2.png")
        self.image = self.open
        self.mouth_open = True

    def tick(self):
        if self.x < 0: # переміщення гравця, проходячи крізь край екрану
            self.x = self.gameInit.width

        if self.x > self.gameInit.width:
            self.x = 0

        self.lastNonCollidingPos = self.getPosition()

        if self.CheckCollision(self.directionBuffer)[0]: # перевірка стикання зі стіною
            self.Move(self.currentDirection)
        else:
            self.Move(self.directionBuffer) # збереження останнього натисненого повороту
            self.currentDirection = self.directionBuffer

        if self.CollidesWall((self.x, self.y)): # уникнення стикання зі стінами
            self.setPosition(self.lastNonCollidingPos[0], self.lastNonCollidingPos[1])
            
    def Move(self, dir: Direction):
        collisionResult = self.CheckCollision(dir)

        desiredPositionCollision = collisionResult[0]
        if not desiredPositionCollision:
            self.lastWorkingDirection = self.currentDirection
            desiredPosition = collisionResult[1]
            self.setPosition(desiredPosition[0], desiredPosition[1])
        else:
            self.currentDirection = self.lastWorkingDirection

    def draw(self):
        self.image = self.open if self.mouth_open else self.closed # зображення відкривання роту
        self.image = pygame.transform.rotate(self.image, self.currentDirection.value)
        super(Player, self).draw()
