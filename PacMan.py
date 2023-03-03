
from GameInit import *
from Field import *
from Player import *
from StaticObjects import *

if __name__ == "__main__":
    UniSize = 32
    game = MazeAndPathController()
    size = game.size
    gameInit = GameInit(size[0] * UniSize, size[1] * UniSize)


    for y, row in enumerate(game.numpy_maze):
        for x, column in enumerate(row):
            if column == 0:
                gameInit.AddWall(Wall(gameInit, x, y, UniSize))

    pacman = Player(gameInit, 32, 32, UniSize)
    gameInit.AddPacman(pacman)
    gameInit.MainLoop(120)

