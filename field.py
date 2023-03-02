import pygame 

class GameObject:
    def __init__(self, surface, x, y, size: int, color=(255, 0, 0), circle: bool = False):
        self.size = size
        self.renderer: Game = surface
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
    
class Wall(GameObject):
    def __init__(self, surface, x, y, size: int, color=(0, 0, 255)):
        super().__init__(surface, x * size, y * size, size, color)
        
class Game:
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

    def tick(self, in_fps: int):
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

    def AddWall(self, obj: Wall):
        self.AddGameObject(obj)
        self.walls.append(obj)
 
class Controller:
    def __init__(self):
        self.ascii_maze = [
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "X            XX            X",
            "X XXXX XXXXX XX XXXXX XXXX X",
            "X                          X",
            "X XXXX XX XXXXXXXX XX XXXX X",
            "X      XX    XX    XX      X",
            "XXXXXX XXXXX XX XXXXX XXXXXX",
            "XXXXXX XX          XX XXXXXX",
            "XXXXXX XX XXX  XXX XX XXXXXX",
            "XXXXXX XX X      X XX XXXXXX",
            "          X      X          ",
            "XXXXXX XX X      X XX XXXXXX",
            "XXXXXX XX XXXXXXXX XX XXXXXX",
            "XXXXXX XX          XX XXXXXX",
            "XXXXXX XX XXXXXXXX XX XXXXXX",
            "X            XX            X",
            "X XXXX XXXXX XX XXXXX XXXX X",
            "X XXXX XXXXX XX XXXXX XXXX X",
            "X   XX                XX   X",
            "XXX XX XX XXXXXXXX XX XX XXX",
            "X      XX    XX    XX      X",
            "X XXXXXXXXXX XX XXXXXXXXXX X",
            "X                          X",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        ]

        self.numpy_maze = []
        self.reachable_spaces = []

        self.size = (0, 0)
        self.convert_maze_to_numpy()

    def convert_maze_to_numpy(self):
        for x, row in enumerate(self.ascii_maze):
            self.size = (len(row), x + 1)
            binary_row = []
            for y, column in enumerate(row):

                if column == "X":
                    binary_row.append(0)
                else:
                    binary_row.append(1)
                    self.reachable_spaces.append((y, x))
                    
            self.numpy_maze.append(binary_row)
            
unified_size = 32
game = Controller()
size = game.size
game_renderer = Game(size[0] * unified_size, size[1] * unified_size)

for y, row in enumerate(game.numpy_maze):
    for x, column in enumerate(row):
        if column == 0:
            game_renderer.AddWall(Wall(game_renderer, x, y, unified_size))

game_renderer.tick(120)