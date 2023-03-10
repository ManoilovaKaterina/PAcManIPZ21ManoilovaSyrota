import numpy as np
import tcod
import random

from GameInit import ScreenToMaze, MazeToScreen
from Ghost import Ghost

class Pathfinder: # знаходження шляху у лабиринті
    def __init__(self, in_arr):
        cost = np.array(in_arr, dtype=np.bool_).tolist()
        self.pf = tcod.path.AStar(cost=cost, diagonal=0) # отримання шляху за допомогою функції бібліотеки tcod

    def get_path(self, from_x, from_y, to_x, to_y):
        res = self.pf.get_path(from_x, from_y, to_x, to_y)
        return [(sub[1], sub[0]) for sub in res] # отримання координат шляху

class MazeAndPathController:
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
            "XXXXXX XX XXXGBXXX XX XXXXXX",
            "XXXXXX XX XBBBBBBX XX XXXXXX",
            "          XBBGGGBX          ",
            "XXXXXX XX XBBBBBBX XX XXXXXX",
            "XXXXXX XX XXXXXXXX XX XXXXXX",
            "XXXXXX XX    P     XX XXXXXX",
            "XXXXXX XX XXXXXXXX XX XXXXXX",
            "X            XX            X",
            "X XXXX XXXXX XX XXXXX XXXX X",
            "X XXXX XXXXX XX XXXXX XXXX X",
            "X   XX                XX   X",
            "XXX XX XX XXXXXXXX XX XX XXX",
            "X      XX    XX    XX      X",
            "X XXXXXXXXXX XX XXXXXXXXXX X",
            "X    O                O    X",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        ]
        self.dotPlace = []
        self.powerupSpace = []
        self.blankSpaces = []
        self.ghost_spawns = []
        self.numpy_maze = []
        self.reachable_spaces = []
        self.size = (0, 0)
        self.MazeToNumpy()
        self.p = Pathfinder(self.numpy_maze)

    def NewRanPath(self, in_ghost: Ghost): # отримання випадкового шляху в лабірінті
        random_space = random.choice(self.dotPlace)
        current_maze_coord = ScreenToMaze(in_ghost.getPosition())

        path = self.p.get_path(current_maze_coord[1], current_maze_coord[0], random_space[1], random_space[0])
        test_path = [MazeToScreen(item) for item in path]
        in_ghost.SetNewPath(test_path)

    def MazeToNumpy(self): # перетворення запису лабірінту в масив
        for x, row in enumerate(self.ascii_maze):
            self.size = (len(row), x + 1)
            binary_row = []
            for y, column in enumerate(row):
                if column == "P":
                    self.hero_spawn = (y, x)
                if column == "G":
                    self.ghost_spawns.append((y, x))
                if column == "X":
                    binary_row.append(0)
                else:
                    binary_row.append(1)
                    if (column != "B") & (column != "G"):
                        self.dotPlace.append((y, x))
                    self.blankSpaces.append((y, x))
                    if column == "O":
                        self.powerupSpace.append((y, x))

            self.numpy_maze.append(binary_row)