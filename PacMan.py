import pygame
import pygame_menu

from GameInit import *
from Field import *
from Ghost import *
from Player import *
from StaticObjects import *

# кольори привидів
GhostColors = [
            "E:/UNI/2 курс/2 семестр/NI_RPZ/RedGhost.png",
            "E:/UNI/2 курс/2 семестр/NI_RPZ/PinkGhost.png",
            "E:/UNI/2 курс/2 семестр/NI_RPZ/OrangeGhost.png",
            "E:/UNI/2 курс/2 семестр/NI_RPZ/BlueGhost.png"
        ]

if __name__ == "__main__":
    UniSize = 32
    game = MazeAndPathController()
    size = game.size
    gameInit = GameInit(size[0] * UniSize, size[1] * UniSize)

    for y, row in enumerate(game.numpy_maze):
        for x, column in enumerate(row):
            if column == 0:
                gameInit.AddWall(Wall(gameInit, x, y, UniSize))
    
    for cookie_space in game.dotPlace:
        translated = MazeToScreen(cookie_space)
        cookie = Cookie(gameInit, translated[0] + UniSize / 2, translated[1] + UniSize / 2)
        gameInit.AddCookie(cookie)
    
    for i, ghost_spawn in enumerate(game.ghost_spawns):
        translated = MazeToScreen(ghost_spawn)
        ghost = Ghost(gameInit, translated[0], translated[1], UniSize, game, GhostColors[i % 4])
        gameInit.AddGhost(ghost)

    pacman = Player(gameInit, 32, 32, UniSize)
    gameInit.AddPacman(pacman)
    gameInit.MainLoop(120)