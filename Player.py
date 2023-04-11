import pygame

from GameInit import GameInit, Direction
from MoveObj import MovableObject


class Player(MovableObject):
    def __init__(self: MovableObject, surf: GameInit,
                 x: int, y: int, initSize: int):
        super().__init__(surf, x, y, initSize, (255, 255, 0))
        self.lastNonCollidingPos = (0, 0)
        self.lastWorkingDirection = Direction.NONE
        self.spawnPoint = [x, y]
        self.open = pygame.image.load("images/PacMan1.png")
        self.closed = pygame.image.load("images/PacMan2.png")
        self.image = self.open
        self.mouth_open = True

    def tick(self: MovableObject):
        if self.x < 0:  # moving the player by passing through the edge of the screen
            self.x = self.gameInit.width

        if self.x > self.gameInit.width:
            self.x = 0

        self.lastNonCollidingPos = self.getPosition()

        # checking for contact with the wall
        if self.CheckCollision(self.directionBuffer, True)[0]:
            self.Move(self.currentDirection)
        else:  # saving the last pressed turn
            self.Move(self.directionBuffer)
            self.currentDirection = self.directionBuffer

        if self.CollidesWall((self.x, self.y), True):
            self.setPosition(self.lastNonCollidingPos[0], 
                             self.lastNonCollidingPos[1])

        self.CookiePickup()
        self.HandleGhosts()

    def Move(self: MovableObject, dir: Direction):
        """
        Переміщує гравця.

        :param dir: напрямок руху гравця.
        """
        collisionResult = self.CheckCollision(dir, True)

        desiredPositionCollision = collisionResult[0]
        # moves the player in the direction where there is no contact with the walls
        if not desiredPositionCollision:
            self.lastWorkingDirection = self.currentDirection
            desiredPosition = collisionResult[1]
            self.setPosition(desiredPosition[0], desiredPosition[1])
        else:  # otherwise, it keeps the previous direction
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

        for cookie in cookies:  # eating point
            collides = collision_rect.colliderect(cookie.getShape())
            if collides and cookie in gameObj:
                gameObj.remove(cookie)
                self.gameInit.score += 10
                cookie_to_remove = cookie

        if cookie_to_remove is not None:
            cookies.remove(cookie_to_remove)

        # win by eating all the points
        if len(self.gameInit.GetCookies()) == 0:
            self.gameInit.win = True

        for powerup in powerups:
            collides = collision_rect.colliderect(powerup.getShape())
            if collides and powerup in gameObj:

                # turning on the power supply
                if not self.gameInit.IsPowerupActive():
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

                # kill the ghost at paverap
                if self.gameInit.IsPowerupActive():
                    ghost.Kill()
                    self.gameInit.GhostRespawn()
                    self.gameInit.score += 400
                else:
                    if not self.gameInit.win:  # kill pacman otherwise
                        self.gameInit.KillPacman()

    def draw(self):

        # image of mouth opening
        self.image = self.open if self.mouth_open else self.closed
        self.image = pygame.transform.rotate(self.image, self.currentDirection.value)
        super(Player, self).draw()
