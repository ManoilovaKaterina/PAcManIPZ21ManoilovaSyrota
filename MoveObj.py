import pygame

from GameInit import GameInit, GameObject, Direction


class MovableObject(GameObject):  # об'єкти, які рухаються
    def __init__(self: GameObject, surf: GameInit, x: int, y: int, initSize: int, initColor=(255, 0, 0)):
        super().__init__(surf, x, y, initSize, initColor)
        self.currentDirection = Direction.NONE
        self.directionBuffer = Direction.NONE  # потрібен для збереженні поворота, якщо кнопку було натиснено раніше
        self.locationQueue = []  # усі доступні розташування
        self.nextTarget = None

    def GetNextLocation(self: GameObject) -> list:
        """
        Отримує наступну координату для руху.

        :return: None при відсутності доступного місця, у іншому випадку - наступна доступна координата
        """
        if len(self.locationQueue) == 0:
            return None
        else:
            self.locationQueue.pop(0)

    def SetDirection(self, dir: Direction):
        """
        Задає напрямок рухомого об'єкта.

        :param dir: задаваємий напрямок.
        """
        self.currentDirection = dir
        self.directionBuffer = dir

    def CollidesWall(self: GameObject, position: list[int], isPacman: bool = False) -> bool:
        """
        Перевіряє стикання зі стінами в даний момент.

        :param position: координата об'єкта, у якій відбудеться перевірки.
        :param isPacman: параметр гравця, який має додатковий об'єкт стикання.

        :return: True при стиканні, False у інакшому випадку.
        """
        collisionRect = pygame.Rect(position[0], position[1], self.size, self.size)
        collides = False
        if isPacman:
            noPlayerSpace = self.gameInit.GetNPS()+self.gameInit.GetWalls()
            for nps in noPlayerSpace:
                collides = collisionRect.colliderect(nps.getShape())
                if collides:
                    break
        else:
            walls = self.gameInit.GetWalls()
            for wall in walls:
                collides = collisionRect.colliderect(wall.getShape())
                if collides:
                    break
        return collides

    def CheckCollision(self: GameObject, dir: Direction, isPacman: bool = False)-> bool:
        """
        Перевіряє, чи відбудеться стикання зі стінами в наступній координаті в напрямку руху.

        :param dir: напрямок руху.
        :param isPacman: параметр гравця, який має додатковий об'єкт стикання.

        :return: True при стиканні, False у інакшому випадку.
        """
        desiredPosition = (0, 0)
        if dir == Direction.NONE:
            return False, desiredPosition
        if dir == Direction.UP:
            desiredPosition = (self.x, self.y - 1)
        elif dir == Direction.DOWN:
            desiredPosition = (self.x, self.y + 1)
        elif dir == Direction.LEFT:
            desiredPosition = (self.x - 1, self.y)
        elif dir == Direction.RIGHT:
            desiredPosition = (self.x + 1, self.y)

        return self.CollidesWall(desiredPosition, isPacman), desiredPosition

    def draw(self):  # промальовка об'єкта
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.surface.blit(self.image, self.getShape())
