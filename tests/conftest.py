import os
import pytest
from PacMan import GhostColors
from Field import diffEasy, MazeAndPathController
from GameInit import GameInit, MazeToScreen
from StaticObjects import Wall
from Player import Player
from Ghost import Ghost

os.environ["SDL_VIDEODRIVER"] = "dummy"


@pytest.fixture()
def initGameForTests():
    field = MazeAndPathController(diffEasy)
    size = field.size

    game = GameInit(size[0]*32, 800)

    for y, row in enumerate(field.numpy_maze):
        for x, column in enumerate(row):
            if column == 0:
                game.AddWall(Wall(game, x, y, 32))
    return game, field


@pytest.fixture()
def initTestPlayer(initGameForTests):
    game, field = initGameForTests
    translated = MazeToScreen(field.hero_spawn)
    pacman = Player(game, translated[0], translated[1], 32)
    game.AddPacman(pacman)
    return pacman


@pytest.fixture()
def initTestGhost(initGameForTests):
    game, field = initGameForTests
    translated = MazeToScreen(field.ghost_spawns[0])
    ghost = Ghost(game, translated[0], translated[1],
                  32, field, GhostColors[0])
    game.AddGhost(ghost)
    return ghost
