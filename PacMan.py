from GameInit import *
from Field import *
from Ghost import *
from Player import *
from StaticObjects import *

# кольори привидів
GhostColors = [
            "C:/Users/undor/sprites/RedGhost.png",
            "C:/Users/undor/sprites/PinkGhost.png",
            "C:/Users/undor/sprites/OrangeGhost.png",
            "C:/Users/undor/sprites/BlueGhost.png"
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
    
    for powerup_space in game.powerupSpace:
        translated = MazeToScreen(powerup_space)
        powerup = Powerup(gameInit, translated[0] + UniSize / 2, translated[1] + UniSize / 2)
        gameInit.AddPowerup(powerup)

    pacman = Player(gameInit, 32, 32, UniSize)
    gameInit.AddPacman(pacman)
    gameInit.MainLoop(120)
