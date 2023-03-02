import pygame
from enum import Enum

GeneralFont = 'C:/Users/undor/sprites/Press_Start_2P/PressStart2P-Regular.ttf'

class GameObject: # загальний клас об'єктів гри
    def __init__(self, surface, x, y, size: int, color=(255, 0, 0), circle: bool = False):
        self.size = size
        self.renderer: GameInit = surface
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

class GameInit:  # ініціалізація параметрів гри
    def __init__(self, in_width: int, in_height: int):
        pygame.init()
        self.width = in_width
        self.height = in_height
        self.screen = pygame.display.set_mode((in_width, in_height))
        pygame.display.set_caption('Pacman')
        self.clock = pygame.time.Clock()
        self.done = False
        self.game_objects = []
        self.walls = []

    def MainLoop(self, in_fps: int):
        black = (0, 0, 0)
        while not self.done:
            for game_object in self.game_objects:
                game_object.tick()
                game_object.draw()

            pygame.display.flip()
            self.clock.tick(in_fps)
            self.screen.fill(black)

    def AddGameObject(self, obj: GameObject):
        self.game_objects.append(obj)

    def AddWall(self, obj: GameObject):
        self.AddGameObject(obj)
        self.walls.append(obj)