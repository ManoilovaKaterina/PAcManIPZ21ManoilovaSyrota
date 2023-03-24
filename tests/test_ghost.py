import pytest
from GameInit import Direction


@pytest.mark.parametrize("loc", [(3, 2), (10, 21), (13, 0), None])
def test_nextloc13(loc, initTestGhost):
    testghost = initTestGhost
    testghost.locationQueue.append(loc)
    assert testghost.GetNextLocation() == loc


@pytest.mark.parametrize("dir", [Direction.UP, Direction.DOWN,
                                 Direction.LEFT, Direction.RIGHT])
def test_ghost_move4(dir, initTestGhost):
    testghost = initTestGhost
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
def test_collides14(dir, initTestGhost):
    testghost = initTestGhost
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
def test_dir15(x, y, initTestGhost):
    testghost = initTestGhost
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
