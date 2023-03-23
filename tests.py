import pytest
from Field import *
from GameInit import *
from PacMan import *

def test_path2():
    print("test path")
    assert MazeAndPathController(diffEasy).p.get_path(11, 0, 13, 1) == [(1, 11), (2, 11), (3, 11), (4, 11), (5, 11), (6, 11), (6, 12), (6, 13), (5, 13), (4, 13), (3, 13), (2, 13), (1, 13)]

def test_arrays3():
    print("test field")
    assert MazeAndPathController(diffEasy).ascii_maze == diffEasy

def test_coords7():
    print("test coords")
    assert MazeToScreen((10, 10)) == (320, 320)

def test_coords8():
    print("test coords")
    assert ScreenToMaze((320, 320)) == (10, 10)

pacman_game = MazeAndPathController(diffEasy)
size = pacman_game.size
UniSize = 32

gameInit = GameInit(size[0] * UniSize, 800)

for y, row in enumerate(pacman_game.numpy_maze):
    for x, column in enumerate(row):
        if column == 0:
            gameInit.AddWall(Wall(gameInit, x, y, UniSize))

translated = MazeToScreen(pacman_game.ghost_spawns[0])
ghost = Ghost(gameInit, translated[0], translated[1], UniSize, pacman_game, GhostColors[0])
gameInit.AddGhost(ghost)

def test_nextloc13():
    ghost.locationQueue.append((3, 2))
    assert ghost.GetNextLocation() == (3, 2)

def test_ghost_move4():
    preLoc = ghost.getPosition()
    
    ghost.Move(Direction.UP)
    dir = Direction.UP

    if dir == Direction.UP:
        preLoc = (preLoc[0], preLoc[1] - 1)
    elif dir == Direction.DOWN:
        preLoc = (preLoc[0], preLoc[1] + 1)
    elif dir == Direction.LEFT:
        preLoc = (preLoc[0] - 1, preLoc[1])
    elif dir == Direction.RIGHT:
        preLoc = (preLoc[0] + 1, preLoc[1])

    assert ghost.getPosition() == preLoc

def test_collides14():
    ghost.setPosition(ghost.spawnPoint[0], ghost.spawnPoint[1]-1)
    assert ghost.CheckCollision(Direction.LEFT) == (True, (415, 351))

def test_dir15():
    assert ghost.DirectionToNextTarget() == Direction.NONE