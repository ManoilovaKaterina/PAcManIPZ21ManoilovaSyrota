from Field import diffEasy, MazeAndPathController
from GameInit import MazeToScreen, ScreenToMaze


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


def test_phases(initGameForTests):
    testgame = initGameForTests[0]
    expphase = testgame.currentPhase + 1
    expchase = not testgame.isChasing
    testgame.ModeSwitch()
    assert expchase == testgame.isChasing, expphase == testgame.currentPhase
