import pytest
from Field import *
from GameInit import *
from PacMan import *

def test_path2():
    expected = [(1, 11), (2, 11), (3, 11), (4, 11), (5, 11), (6, 11), (6, 12), (6, 13), (5, 13), (4, 13), (3, 13), (2, 13), (1, 13)]
    assert MazeAndPathController(diffEasy).p.get_path(11, 0, 13, 1) == expected

def test_arrays3():
    assert MazeAndPathController(diffEasy).ascii_maze == diffEasy

def test_maze_t_screen7():
    assert MazeToScreen((10, 10)) == (320, 320)

def test_screen_to_maze8():
    assert ScreenToMaze((320, 320)) == (10, 10)

global testghost
global testpacman

def initGameForTests():
    global testghost
    global testpacman
    pacman_game = MazeAndPathController(diffEasy)
    size = pacman_game.size
    UniSize = 32

    gameInit = GameInit(size[0] * UniSize, 800)

    for y, row in enumerate(pacman_game.numpy_maze):
        for x, column in enumerate(row):
            if column == 0:
                gameInit.AddWall(Wall(gameInit, x, y, UniSize))

    translated = MazeToScreen(pacman_game.ghost_spawns[0])
    testghost = Ghost(gameInit, translated[0], translated[1], UniSize, pacman_game, GhostColors[0])
    gameInit.AddGhost(testghost)

    testpacman = Player(gameInit, translated[0], translated[1], UniSize)
    gameInit.AddPacman(testpacman)
    # gameInit.isChasing = True
    # gameInit.MainLoop(120)

initGameForTests()

def test_nextloc13():
    testghost.locationQueue.append((3, 2))
    assert testghost.GetNextLocation() == (3, 2)

@pytest.mark.parametrize("dir", [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])
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

def test_collides14():
    testghost.setPosition(testghost.spawnPoint[0], testghost.spawnPoint[1]-1)
    assert testghost.CheckCollision(Direction.LEFT) == (True, (415, 351))

def test_dir15():
    assert testghost.DirectionToNextTarget() == Direction.NONE