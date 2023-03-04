import pygame
from enum import Enum

GeneralFont = 'C:/Users/undor/sprites/Press_Start_2P/PressStart2P-Regular.ttf'

class Direction(Enum): # клас для визначення напрямку руху
    DOWN = -90
    RIGHT = 0
    UP = 90
    LEFT = 180
    NONE = 360
    
class GameObject: # загальний клас об'єктів гри
    def __init__(self, surface, x, y, size: int, color=(255, 0, 0), circle: bool = False):
        self.size = size
        self.gameInit: GameInit = surface
        self.surface = surface.screen
        self.y = y
        self.x = x
        self.color = color
        self.circle = circle
        self.shape = pygame.Rect(self.x, self.y, size, size)

    def draw(self):
        if self.circle:
            pygame.draw.circle(self.surface, self.color, (self.x, self.y), self.size)
        else:
            rect_object = pygame.Rect(self.x, self.y, self.size, self.size)
            pygame.draw.rect(self.surface, self.color, rect_object, border_radius=4)

    def tick(self):
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
        pygame.init()
        self.width = initWidth
        self.height = initHeight
        self.screen = pygame.display.set_mode((initWidth, initHeight))
        pygame.display.set_caption('Pacman')
        self.clock = pygame.time.Clock()
        self.pacman = None
        self.done = False
        self.score = 0
        self.cookies = []
        self.gameObjects = []
        self.walls = []
        self.mouthOpenEvent = pygame.USEREVENT + 1

    def MainLoop(self, in_fps: int):
        color = (0, 0, 0)
        pygame.time.set_timer(self.mouthOpenEvent, 200)
        while not self.done:
            for game_object in self.gameObjects:
                game_object.tick()
                game_object.draw()

            pygame.display.flip()
            self.clock.tick(in_fps)
            self.screen.fill(color)
            self.HandleEvents()

    def AddGameObject(self, obj: GameObject):
        self.gameObjects.append(obj)

    def AddWall(self, obj: GameObject):
        self.AddGameObject(obj)
        self.walls.append(obj)

    def AddPacman(self, initHero):
        self.AddGameObject(initHero)
        self.pacman = initHero

    def AddCookie(self, obj: GameObject):
        self.gameObjects.append(obj)
        self.cookies.append(obj)

    def GetWalls(self):
        return self.walls
    
    def GetCookies(self):
        return self.cookies
    
    def GetGameObjects(self):
        return self.gameObjects    
    
    def HandleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

            if event.type == self.mouthOpenEvent: # подія для анімації відкривання роту пакмана
                if self.pacman is None: break
                self.pacman.mouth_open = not self.pacman.mouth_open

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.pacman.SetDirection(Direction.UP)
        elif pressed[pygame.K_LEFT]:
            self.pacman.SetDirection(Direction.LEFT)
        elif pressed[pygame.K_DOWN]:
            self.pacman.SetDirection(Direction.DOWN)
        elif pressed[pygame.K_RIGHT]:
            self.pacman.SetDirection(Direction.RIGHT)

def ScreenToMaze(initCoords, initSize=32): # дістає безпосередні координати у лабиринті
    return int(initCoords[0] / initSize), int(initCoords[1] / initSize)

def MazeToScreen(initCoords, initSize=32): # перетворює координати у вигляд подання на екрані
    return initCoords[0] * initSize, initCoords[1] * initSize