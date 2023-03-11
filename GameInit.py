import pygame
from enum import Enum

GeneralFont = 'E:/UNI/2 курс/2 семестр/NI_RPZ/PressStart2P-Regular.ttf'

class Direction(Enum): # клас для визначення напрямку руху
    DOWN = -90
    RIGHT = 0
    UP = 90
    LEFT = 180
    NONE = 360
    
class GameObject: # загальний клас об'єктів гри
    def __init__(self, surf, x, y, initSize: int, initColor=(0, 0, 0), isCircle: bool = False):
        self.size = initSize
        self.y = y
        self.x = x
        self.color = initColor
        self.circle = isCircle
        self.gameInit: GameInit = surf # параметри гри
        self.surface = surf.screen # площа екрану
        self.shape = pygame.Rect(self.x, self.y, initSize, initSize) # форма об'єкта, стандартна - квадрат

    def draw(self): # безпосередньо промальовка об'єкту
        if self.circle:
            pygame.draw.circle(self.surface, self.color, (self.x, self.y), self.size)
        else:
            rectangle = pygame.Rect(self.x, self.y, self.size, self.size)
            pygame.draw.rect(self.surface, self.color, rectangle, border_radius = 4)

    def tick(self): # поведінка об'єкту на кожному кадрі
        pass

    def getShape(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def setPosition(self, in_x, in_y): # задання положення об'єкту
        self.x = in_x
        self.y = in_y

    def getPosition(self):
        return (self.x, self.y)

class GameInit:  # ініціалізація параметрів гри
    def __init__(self, initWidth: int, initHeight: int):
        self.width = initWidth
        self.height = initHeight
        self.screen = pygame.display.set_mode((initWidth, initHeight))
        self.clock = pygame.time.Clock() # початок відліку часу
        self.done = False
        self.win = False
        self.gameObjects = []
        self.walls = []
        self.cookies = []
        self.powerups = []
        self.ghosts = []
        self.pacman = None
        self.lives = 3
        self.score = 0
        self.powerupActive = False
        self.isChasing = False
        self.modeSwitchEvent = pygame.USEREVENT + 1 # задаємо додаткові події
        self.powerupEndEvent = pygame.USEREVENT + 2
        self.mouthOpenEvent = pygame.USEREVENT + 3
        self.ghostRespawnEvent = pygame.USEREVENT + 4
        self.modes = [(7, 20),(7, 20),(5, 20),(5, 999999)] # зміна фаз гри, від якої залежить поведінка привидів
        self.currentPhase = 0

    def MainLoop(self, initfps: int): # головний цикл гри
        self.ModeSwitch() # зміна фаз гри
        pygame.time.set_timer(self.mouthOpenEvent, 200)
        while not self.done:
            for game_object in self.gameObjects:
                game_object.tick()
                game_object.draw()

            self.DisplayText(f"[Score: {self.score}]  [Lives: {self.lives}]") # показуємо кількість очків та життів

            if self.pacman is None: # завершаємо гру, якщо гравця вбито, або рахуємо перемогу у її випадку
                self.DisplayText("GAME OVER", (self.width / 2 - 256, self.height / 2 - 256), 60)
            if self.win:
                self.DisplayText("YOU WON", (self.width / 2 - 256, self.height / 2 - 256), 60)
            pygame.display.flip()
            self.clock.tick(initfps) # кадрів в секунду
            self.screen.fill((1, 14, 18)) # заповнюємо фон кольором
            self.HandleEvents()

    def Pause(self):
        loop = 1
        self.DisplayText("PAUSE", (self.width / 2 - 150, self.height / 2 - 150), 60)
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
            self.clock.tick(60)

    def ModeSwitch(self): # зміна фаз гри
        currentPhaseTime = self.modes[self.currentPhase]
        scatterTime = currentPhaseTime[0] # час блукання привидів без цілі
        chaseTime = currentPhaseTime[1] # час переслідування равця привидами

        if self.isChasing == True:
            self.currentPhase += 1
            self.isChasing = False
        else:
            self.isChasing = True

        if self.isChasing == False:
            usedTime = scatterTime
        else:
            usedTime = chaseTime
        pygame.time.set_timer(self.modeSwitchEvent, usedTime * 1000) # відлік часу до наступної зміни фази

    # додавання об'єктів у гру
    def AddCookie(self, obj: GameObject):
        self.gameObjects.append(obj)
        self.cookies.append(obj)

    def AddGhost(self, obj: GameObject):
        self.gameObjects.append(obj)
        self.ghosts.append(obj)

    def AddPowerup(self, obj: GameObject):
        self.gameObjects.append(obj)
        self.powerups.append(obj)

    def AddWall(self, obj: GameObject):
        self.gameObjects.append(obj)
        self.walls.append(obj)
    
    def AddPacman(self, in_hero):
        self.gameObjects.append(in_hero)
        self.pacman = in_hero

    def SetPowerupTime(self): # відлік часу паверапу
        pygame.time.set_timer(self.powerupEndEvent, 10000)
    
    def ActivatePowerup(self): # активація паверапу
        self.powerupActive = True
        self.isChasing = False
        self.SetPowerupTime()

    def EndGame(self): # завершення гри
        if self.pacman in self.gameObjects:
            self.gameObjects.remove(self.pacman)
        self.pacman = None

    def KillPacman(self): # вбити гравця
        self.lives -= 1
        self.pacman.setPosition(self.pacman.spawnPoint[0], self.pacman.spawnPoint[1]) # переміщення гравця у початкову позицію
        for ghost in self.ghosts: # повернення привидів до початкового стану
            ghost.__init__(self, ghost.spawnPoint[0], ghost.spawnPoint[1], 32, ghost.gameController, ghost.spritePath)
        self.pacman.SetDirection(Direction.NONE)
        if self.lives == 0:
            self.EndGame() # завершення гри якщо життя закінчились
    
    def GhostRespawn(self): # відлік часу респавну привидів
        pygame.time.set_timer(self.ghostRespawnEvent, 5000)

    def DisplayText(self, text, in_position=(32, 7), initSize=20):
        font = pygame.font.Font(GeneralFont, initSize)
        text_surface = font.render(text, False, (255, 255, 255))
        self.screen.blit(text_surface, in_position)

    # отримання параметрів гри
    def IsPowerupActive(self):
        return self.powerupActive

    def GetWalls(self):
        return self.walls

    def GetCookies(self):
        return self.cookies
    
    def GetGhosts(self):
        return self.ghosts

    def GetPowerups(self):
        return self.powerups

    def GetGameObjects(self):
        return self.gameObjects
    
    def GetPacmanPosition(self):
        return self.pacman.getPosition() if self.pacman != None else (0, 0)

    # управління та робота з подіями гри
    def HandleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

            if event.type == self.modeSwitchEvent:
                self.ModeSwitch()

            if event.type == self.powerupEndEvent:
                self.powerupActive = False

            if event.type == self.ghostRespawnEvent:
                for ghost in self.ghosts:
                    if ghost.dead == True: # повернення мертвих привидів до початкового стану 
                        ghost.__init__(self, ghost.spawnPoint[0], ghost.spawnPoint[1], 31, ghost.gameController, ghost.spritePath)

            if event.type == self.mouthOpenEvent: # подія для анімації відкривання роту пакмана
                if self.pacman is None: break
                self.pacman.mouth_open = not self.pacman.mouth_open

        # управління
        pressed = pygame.key.get_pressed()
        if self.pacman is None: return
        if pressed[pygame.K_UP]:
            self.pacman.SetDirection(Direction.UP)
        elif pressed[pygame.K_LEFT]:
            self.pacman.SetDirection(Direction.LEFT)
        elif pressed[pygame.K_DOWN]:
            self.pacman.SetDirection(Direction.DOWN)
        elif pressed[pygame.K_RIGHT]:
            self.pacman.SetDirection(Direction.RIGHT)
        if pressed[pygame.K_ESCAPE]:
            self.Pause()

def ScreenToMaze(initCoords, initSize=32): # дістає безпосередні координати у лабиринті
    return int(initCoords[0] / initSize), int(initCoords[1] / initSize)

def MazeToScreen(initCoords, initSize=32): # перетворює координати у вигляд подання на екрані
    return initCoords[0] * initSize, initCoords[1] * initSize