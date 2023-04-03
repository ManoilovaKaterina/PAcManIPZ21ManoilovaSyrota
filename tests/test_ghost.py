import pytest
from GameInit import Direction


@pytest.mark.parametrize("loc", [(3, 2), (10, 21), (13, 0), None])
def test_next_loc(loc, initTestGhost):
    initTestGhost.locationQueue.append(loc)
    assert initTestGhost.GetNextLocation() == loc


@pytest.mark.movement
@pytest.mark.parametrize("dir", [Direction.UP, Direction.DOWN,
                                 Direction.LEFT, Direction.RIGHT])
def test_ghost_move(dir, initTestGhost):
    initTestGhost
    initTestGhost.setPosition(6, 11)
    preLoc = initTestGhost.getPosition()
    initTestGhost.Move(dir)

    if dir == Direction.UP:
        preLoc = (preLoc[0], preLoc[1] - 1)
    elif dir == Direction.DOWN:
        preLoc = (preLoc[0], preLoc[1] + 1)
    elif dir == Direction.LEFT:
        preLoc = (preLoc[0] - 1, preLoc[1])
    elif dir == Direction.RIGHT:
        preLoc = (preLoc[0] + 1, preLoc[1])

    assert initTestGhost.getPosition() == preLoc


@pytest.mark.collision
@pytest.mark.parametrize("dir", [Direction.UP, Direction.DOWN,
                                 Direction.LEFT, Direction.RIGHT])
def test_ghost_collides(dir, initTestGhost):
    initTestGhost
    initTestGhost.setPosition(initTestGhost.spawnPoint[0],
                              initTestGhost.spawnPoint[1])
    if dir == Direction.UP:
        expected = (True, (416, 351))
    elif dir == Direction.DOWN:
        expected = (True, (416, 353))
    elif dir == Direction.LEFT:
        expected = (False, (415, 352))
    else:
        expected = (False, (417, 352))
    assert initTestGhost.CheckCollision(dir) == expected


@pytest.mark.parametrize("x, y",
                         [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 0), (1, 1)])
def test_ghost_dir(x, y, initTestGhost):
    initTestGhost
    initTestGhost.nextTarget = (initTestGhost.getPosition()[0]+x,
                                initTestGhost.getPosition()[1]+y)

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
    assert initTestGhost.DirectionToNextTarget() == expected
