import pytest
from Field import diffEasy, MazeAndPathController
from GameInit import GameInit, MazeToScreen, ScreenToMaze, Direction
from PacMan import GhostColors
from StaticObjects import Wall
from Ghost import Ghost
from Player import Player


global testghost
global testpacman
global testgame


def test_path2():
    expected = [(1, 11), (2, 11), (3, 11), (4, 11), (5, 11), (6, 11), (6, 12),
                (6, 13), (5, 13), (4, 13), (3, 13), (2, 13), (1, 13)]
    assert MazeAndPathController(diffEasy).p.get_path(11, 0, 13, 1) == expected


def test_arrays3():
    assert MazeAndPathController(diffEasy).ascii_maze == diffEasy


def test_maze_to_screen7():
    assert MazeToScreen((10, 10)) == (320, 320)


def test_screen_to_maze8():
    assert ScreenToMaze((320, 320)) == (10, 10)


def initGameForTests():
    global testghost
    global testpacman
    global testgame

    pacman_game = MazeAndPathController(diffEasy)
    size = pacman_game.size
    UniSize = 32

    testgame = GameInit(size[0] * UniSize, 800)

    for y, row in enumerate(pacman_game.numpy_maze):
        for x, column in enumerate(row):
            if column == 0:
                testgame.AddWall(Wall(testgame, x, y, UniSize))

    translated = MazeToScreen(pacman_game.ghost_spawns[0])
    testghost = Ghost(testgame, translated[0], translated[1],
                      UniSize, pacman_game, GhostColors[0])
    testgame.AddGhost(testghost)

    testpacman = Player(testgame, translated[0], translated[1], UniSize)
    testgame.AddPacman(testpacman)


initGameForTests()


@pytest.mark.parametrize("loc", [(3, 2), (10, 21), (13, 0), None])
def test_nextloc13(loc):
    testghost.locationQueue.append(loc)
    assert testghost.GetNextLocation() == loc


@pytest.mark.parametrize("dir", [Direction.UP, Direction.DOWN,
                                 Direction.LEFT, Direction.RIGHT])
def test_ghost_move4(dir):
    testghost.setPosition(6, 11)
    preLoc = testghost.getPosition()
    testghost.Move(dir)

    if dir == Direction.UP:
        preLoc = (preLoc[0], preLoc[1] - 1)
    elif dir == Direction.DOWN:
        preLoc = (preLoc[0], preLoc[1] + 1)
    elif dir == Direction.LEFT:
        preLoc = (preLoc[0] - 1, preLoc[1])
    elif dir == Direction.RIGHT:
        preLoc = (preLoc[0] + 1, preLoc[1])

    assert testghost.getPosition() == preLoc


@pytest.mark.parametrize("dir", [Direction.UP, Direction.DOWN,
                                 Direction.LEFT, Direction.RIGHT])
def test_collides14(dir):
    testghost.setPosition(testghost.spawnPoint[0], testghost.spawnPoint[1])
    if dir == Direction.UP:
        expected = (True, (416, 351))
    elif dir == Direction.DOWN:
        expected = (True, (416, 353))
    elif dir == Direction.LEFT:
        expected = (False, (415, 352))
    else:
        expected = (False, (417, 352))
    assert testghost.CheckCollision(dir) == expected


@pytest.mark.parametrize("x, y",
                         [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 0), (1, 1)])
def test_dir15(x, y):
    testghost.nextTarget = (testghost.getPosition()[0]+x,
                            testghost.getPosition()[1]+y)

    if (x == 0):
        if y > 0:
            expected = Direction.DOWN
        else:
            expected = Direction.UP
    elif (y == 0):
        if x > 0:
            expected = Direction.RIGHT
        else:
            expected = Direction.LEFT
    else:
        expected = Direction.NONE
    assert testghost.DirectionToNextTarget() == expected


def test_phases():
    expphase = testgame.currentPhase + 1
    expchase = not testgame.isChasing
    testgame.ModeSwitch()
    assert expchase == testgame.isChasing, expphase == testgame.currentPhase
