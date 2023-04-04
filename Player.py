import pygame

from GameInit import GameInit, Direction
from MoveObj import MovableObject


class Player(MovableObject):
    def __init__(self: MovableObject, surf: GameInit, x: int, y: int, initSize: int):
        super().__init__(surf, x, y, initSize, (255, 255, 0))
        self.lastNonCollidingPos = (0, 0)
        self.spawnPoint = [x, y]
        self.open = pygame.image.load("images/PacMan1.png")
        self.closed = pygame.image.load("images/PacMan2.png")
        self.image = self.open
        self.mouth_open = True

    def tick(self: MovableObject):
        if self.x < 0:  # переміщення гравця, проходячи крізь край екрану
            self.x = self.gameInit.width

        if self.x > self.gameInit.width:
            self.x = 0

        self.lastNonCollidingPos = self.getPosition()

        if self.CheckCollision(self.directionBuffer, True)[0]:  # перевірка стикання зі стіною
            self.Move(self.currentDirection)
        else:
            self.Move(self.directionBuffer) # збереження останнього натисненого повороту
            self.currentDirection = self.directionBuffer

        if self.CollidesWall((self.x, self.y), True): # уникнення стикання зі стінами
            self.setPosition(self.lastNonCollidingPos[0], self.lastNonCollidingPos[1])

        self.CookiePickup()
        self.HandleGhosts()

    def Move(self: MovableObject, dir: Direction):
        """
        Переміщує гравця.

        :param dir: напрямок руху гравця.
        """
        collisionResult = self.CheckCollision(dir, True)

        desiredPositionCollision = collisionResult[0]
        if not desiredPositionCollision:  # рухає гравця в ту сторону, де нема стикання зі стінами
            self.lastWorkingDirection = self.currentDirection
            desiredPosition = collisionResult[1]
            self.setPosition(desiredPosition[0], desiredPosition[1])
        else:  # у іншому випадку зберігає попередній напрямок
            self.currentDirection = self.lastWorkingDirection

    def CookiePickup(self:  MovableObject):
        """
        Відтворює з'їдання точки та паверапу.
        """
        collision_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        cookies = self.gameInit.GetCookies()
        powerups = self.gameInit.GetPowerups()
        gameObj = self.gameInit.GetGameObjects()
        cookie_to_remove = None

        for cookie in cookies:  # з'їдання точки
            collides = collision_rect.colliderect(cookie.getShape())
            if collides and cookie in gameObj:
                gameObj.remove(cookie)
                self.gameInit.score += 10
                cookie_to_remove = cookie

        if cookie_to_remove is not None:
            cookies.remove(cookie_to_remove)

        if len(self.gameInit.GetCookies()) == 0:  # перемога при з'їданні усіх точок
            self.gameInit.win = True

        for powerup in powerups:
            collides = collision_rect.colliderect(powerup.getShape())
            if collides and powerup in gameObj:
                if not self.gameInit.IsPowerupActive():  # вмикання паверапу
                    gameObj.remove(powerup)
                    self.gameInit.score += 50
                    self.gameInit.ActivatePowerup()

    def HandleGhosts(self: MovableObject):
        """ Відтворює стикання з привидами."""
        collision_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        ghosts = self.gameInit.GetGhosts()
        gameObj = self.gameInit.GetGameObjects()
        for ghost in ghosts:
            collides = collision_rect.colliderect(ghost.getShape())
            if collides and ghost in gameObj:
                if self.gameInit.IsPowerupActive():  # вбити привида при паверапі
                    ghost.Kill()
                    self.gameInit.GhostRespawn()
                    self.gameInit.score += 400
                else:
                    if not self.gameInit.win:  # вбити пакмена у іншому випадку
                        self.gameInit.KillPacman()

    def draw(self):
        self.image = self.open if self.mouth_open else self.closed  # зображення відкривання роту
        self.image = pygame.transform.rotate(self.image, self.currentDirection.value)
        super(Player, self).draw()
