import pygame

from GameInit import *
from Field import *
from StaticObjects import *

if __name__ == "__main__":
    unified_size = 32
    game = MazeAndPathController()
    size = game.size
    game_renderer = GameInit(size[0] * unified_size, size[1] * unified_size)

    for y, row in enumerate(game.numpy_maze):
        for x, column in enumerate(row):
            if column == 0:
                game_renderer.AddWall(Wall(game_renderer, x, y, unified_size))

    game_renderer.MainLoop(120)