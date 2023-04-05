import pygame
from enum import Enum

GeneralFont = 'text/Press_Start_2P/PressStart2P-Regular.ttf'


class Direction(Enum):  # class for determining the direction of movement
    DOWN = -90
    RIGHT = 0
    UP = 90
    LEFT = 180
    NONE = 360


class GameObject:  # general class of game objects
    def __init__(self, surf, x: int, y: int, initSize: int, initColor=(0, 0, 0), isCircle: bool = False):
        self.size = initSize
        self.y = y
        self.x = x
        self.color = initColor
        self.circle = isCircle
        self.gameInit: GameInit = surf  # game parameters
        self.surface = surf.screen  # screen area

        # object shape, standard - square
        self.shape = pygame.Rect(self.x, self.y, initSize, initSize)

    def draw(self):
        """ Промальовка об'єкту. """
        if self.circle:
            pygame.draw.circle(self.surface, self.color, (self.x, self.y), self.size)
        else:
            rectangle = pygame.Rect(self.x, self.y, self.size, self.size)
            pygame.draw.rect(self.surface, self.color, rectangle, border_radius = 4)

    def tick(self):
        """ Поведінка об'єкту на кожному кадрі """
        pass

    def getShape(self):
        """
        :return: форма об'єкту.
        """
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def setPosition(self, in_x: int, in_y: int):
        """ Задає положення об'єкту. """
        self.x = in_x
        self.y = in_y

    def getPosition(self) -> list:
        """
        :return: Отримує положення об'єкту.
        """
        return (self.x, self.y)


class GameInit:  # initialization of game parameters
    def __init__(self, initWidth: int, initHeight: int):
        self.width = initWidth
        self.height = initHeight
        self.screen = pygame.display.set_mode((initWidth, initHeight))
        self.clock = pygame.time.Clock()  # the start of the countdown
        self.done = False
        self.win = False
        self.gameObjects = []
        self.walls = []
        self.cookies = []
        self.powerups = []
        self.ghosts = []
        self.nps = []
        self.pacman = None
        self.lives = 3
        self.score = 0
        self.powerupActive = False
        self.isChasing = False
        self.modeSwitchEvent = pygame.USEREVENT + 1  # set additional events
        self.powerupEndEvent = pygame.USEREVENT + 2
        self.mouthOpenEvent = pygame.USEREVENT + 3
        self.ghostRespawnEvent = pygame.USEREVENT + 4

        # changing the phases of the game, which depends on the behavior of ghosts
        self.modes = [(7, 20), (7, 20), (5, 20), (5, 999999)]
        self.currentPhase = 0

    def MainLoop(self, initfps: int):
        """
        Головний цикл гри.

        :param initfps: к-ть кадрів в секунду.
        """
        self.ModeSwitch()  # change of game phases
        pygame.time.set_timer(self.mouthOpenEvent, 200)
        while not self.done:
            for game_object in self.gameObjects:
                game_object.tick()
                game_object.draw()

            # show the number of points and lives
            self.DisplayText(f"[Score: {self.score}]  [Lives: {self.lives}]")
            pressed = pygame.key.get_pressed()

            # end the game if the player is killed, or count the victory in her case
            if self.pacman is None:
                self.DisplayText("GAME OVER", (self.width / 2 - 256, self.height / 2 - 256), 60)
                self.DisplayText("press SPACE or ESC to return to main menu", (self.width / 2 - 286, self.height / 2 - 156), 15)
                if (pressed[pygame.K_ESCAPE]) or (pressed[pygame.K_SPACE]):
                    self.done = True
            if self.win:
                self.DisplayText("YOU WON", (self.width / 2 - 256, self.height / 2 - 256), 60)
                self.DisplayText("press SPACE or ESC to return to main menu", (self.width / 2 - 286, self.height / 2 - 156), 15)
                if (pressed[pygame.K_ESCAPE]) or (pressed[pygame.K_SPACE]):
                    self.done = True
            pygame.display.flip()
            self.clock.tick(initfps)  # frames per second
            self.screen.fill((1, 14, 18))  # fill the background with color
            self.HandleEvents()

    def Pause(self):
        """ Пауза. """
        loop = 1
        self.DisplayText("PAUSE", (self.width / 2 - 150, self.height / 2 - 150), 60)
        self.DisplayText("press SPACE to continue or ESC to return to main menu", (self.width / 2 - 396, self.height / 2 - 56), 15)
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.done = True
                        loop = 0
                    if event.key == pygame.K_SPACE:
                        self.screen.fill((0, 0, 0))
                        loop = 0
            pygame.display.update()
            self.clock.tick(120)

    def ModeSwitch(self):
        """ Зміна режимів поведінки привидів. """
        currentPhaseTime = self.modes[self.currentPhase]
        scatterTime = currentPhaseTime[0]  # the time of ghosts wandering aimlessly
        chaseTime = currentPhaseTime[1]  # the time of ghost haunting

        if self.isChasing:
            self.currentPhase += 1
            self.isChasing = False
        else:
            self.isChasing = True

        if not self.isChasing:
            usedTime = scatterTime
        else:
            usedTime = chaseTime

        # countdown to the next phase change
        pygame.time.set_timer(self.modeSwitchEvent, usedTime * 1000)  

    # adding objects to the game
    def AddCookie(self, obj: GameObject):
        """ Додає точку. """
        self.gameObjects.append(obj)
        self.cookies.append(obj)

    def AddGhost(self, obj: GameObject):
        """ Додає привида."""
        self.gameObjects.append(obj)
        self.ghosts.append(obj)

    def AddPowerup(self, obj: GameObject):
        """ Додає паверап."""
        self.gameObjects.append(obj)
        self.powerups.append(obj)

    def AddWall(self, obj: GameObject):
        """ Додає стіну."""
        self.gameObjects.append(obj)
        self.walls.append(obj)

    def AddNPS(self, obj: GameObject):
        """ Додає місце, недоступне для гравця."""
        self.gameObjects.append(obj)
        self.nps.append(obj)

    def AddPacman(self, in_hero):
        """ Додає гравця."""
        self.gameObjects.append(in_hero)
        self.pacman = in_hero

    def SetPowerupTime(self):
        """ Відлік часу паверапу."""
        pygame.time.set_timer(self.powerupEndEvent, 10000)

    def ActivatePowerup(self):
        """ Активує паверап."""
        self.powerupActive = True
        self.isChasing = False
        self.SetPowerupTime()

    def EndGame(self):
        """ Завершує гру."""
        if self.pacman in self.gameObjects:
            self.gameObjects.remove(self.pacman)
        self.pacman = None

    def KillPacman(self):
        """ Вбиває гравця."""
        self.lives -= 1

        # moving the player to the starting position
        self.pacman.setPosition(self.pacman.spawnPoint[0], self.pacman.spawnPoint[1])
        for ghost in self.ghosts:  # returning ghosts to their original state
            ghost.__init__(self, ghost.spawnPoint[0], ghost.spawnPoint[1], 32, ghost.gameController, ghost.spritePath)
        self.pacman.SetDirection(Direction.NONE)
        if self.lives == 0:
            self.EndGame()  # game over if lives run out

    def GhostRespawn(self):
        """ Відлік часу респавну привидів."""
        pygame.time.set_timer(self.ghostRespawnEvent, 5000)

    def DisplayText(self, text, in_position=(32, 7), initSize=20):
        """ Відображвє тексту."""
        font = pygame.font.Font(GeneralFont, initSize)
        text_surface = font.render(text, False, (255, 255, 255))
        self.screen.blit(text_surface, in_position)

    # getting game parameters
    def IsPowerupActive(self):
        return self.powerupActive

    def GetWalls(self):
        return self.walls

    def GetNPS(self):
        return self.nps

    def GetCookies(self):
        return self.cookies

    def GetGhosts(self):
        return self.ghosts

    def GetPowerups(self):
        return self.powerups

    def GetGameObjects(self):
        return self.gameObjects

    def GetPacmanPosition(self):
        return self.pacman.getPosition() if self.pacman is not None else (0, 0)

    def HandleEvents(self):
        """Управління гравцем та робота з подіями гри."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

            if event.type == self.modeSwitchEvent:
                self.ModeSwitch()

            if event.type == self.powerupEndEvent:
                self.powerupActive = False

            if event.type == self.ghostRespawnEvent:
                for ghost in self.ghosts:

                    # returning dead ghosts to their original state
                    if ghost.dead:
                        ghost.__init__(self, ghost.spawnPoint[0], ghost.spawnPoint[1], 31, ghost.gameController, ghost.spritePath)

            # event for pacman mouth opening animation
            if event.type == self.mouthOpenEvent:

                if self.pacman is None:
                    break
                self.pacman.mouth_open = not self.pacman.mouth_open

        # control
        pressed = pygame.key.get_pressed()
        if self.pacman is None:
            return
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            self.pacman.SetDirection(Direction.UP)
        elif pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            self.pacman.SetDirection(Direction.LEFT)
        elif pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            self.pacman.SetDirection(Direction.DOWN)
        elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.pacman.SetDirection(Direction.RIGHT)
        if pressed[pygame.K_ESCAPE]:
            self.Pause()


def ScreenToMaze(initCoords, initSize=32):
    """:return: перетворені координати екрану на безпосередні координати у лабиринті"""
    return int(initCoords[0] / initSize), int(initCoords[1] / initSize)


def MazeToScreen(initCoords, initSize=32):
    """:return: перетворені координати лабірінту у вигляд подання на екрані."""
    return initCoords[0] * initSize, initCoords[1] * initSize
