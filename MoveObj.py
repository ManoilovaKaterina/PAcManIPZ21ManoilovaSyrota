import pygame

from GameInit import *

class MovableObject(GameObject): # об'єкти, які рухаються
    def __init__(self, surf, x, y, initSize: int, initColor=(255, 0, 0)):
        super().__init__(surf, x, y, initSize, initColor)
        self.currentDirection = Direction.NONE
        self.directionBuffer = Direction.NONE # потрібен для збереженні поворота, якщо кнопку було натиснено раніше
        self.locationQueue = [] # усі доступні розташування
        self.nextTarget = None

    def GetNextLocation(self):
        return None if len(self.locationQueue) == 0 else self.locationQueue.pop(0) # видалення пройденого шляху

    def SetDirection(self, dir): # задання повороту
        self.currentDirection = dir
        self.directionBuffer = dir

    def CollidesWall(self, position): # стикання зі стінами
        collisionRect = pygame.Rect(position[0], position[1], self.size, self.size)
        collides = False
        walls = self.gameInit.GetWalls()
        for wall in walls:
            collides = collisionRect.colliderect(wall.getShape())
            if collides: break
        return collides

    def CheckCollision(self, dir: Direction): # перевірення стикання зі стінами
        desiredPosition = (0, 0)
        if dir == Direction.NONE: return False, desiredPosition
        if dir == Direction.UP:
            desiredPosition = (self.x, self.y - 1)
        elif dir == Direction.DOWN:
            desiredPosition = (self.x, self.y + 1)
        elif dir == Direction.LEFT:
            desiredPosition = (self.x - 1, self.y)
        elif dir == Direction.RIGHT:
            desiredPosition = (self.x + 1, self.y)

        return self.CollidesWall(desiredPosition), desiredPosition

    def draw(self): # промальовка об'єкта
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.surface.blit(self.image, self.getShape())
