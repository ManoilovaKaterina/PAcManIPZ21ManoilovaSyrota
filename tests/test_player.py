import pytest
from GameInit import Direction


@pytest.mark.movement
@pytest.mark.parametrize("dir", [Direction.UP, Direction.DOWN,
                                 Direction.LEFT, Direction.RIGHT])
def test_player_move(dir, initTestPlayer):
    preLoc = initTestPlayer.getPosition()
    initTestPlayer.Move(dir)

    if dir == Direction.LEFT:
        preLoc = (preLoc[0] - 1, preLoc[1])
    elif dir == Direction.RIGHT:
        preLoc = (preLoc[0] + 1, preLoc[1])

    assert initTestPlayer.getPosition() == preLoc


@pytest.mark.collision
@pytest.mark.parametrize("isPA", [True,  False])
def test_player_collides(isPA, initTestGhost, initTestPlayer):
    initTestPlayer.gameInit.powerupActive = isPA
    initTestGhost.gameInit = initTestPlayer.gameInit
    initTestGhost.setPosition(initTestPlayer.spawnPoint[0],
                              initTestPlayer.spawnPoint[1])
    initTestPlayer.HandleGhosts()

    if isPA:
        test = initTestPlayer.gameInit.score
        expected = 400
    else:
        test = initTestPlayer.gameInit.lives
        expected = 2
    assert test == expected


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
