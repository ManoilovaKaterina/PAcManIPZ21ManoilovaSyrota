import pygame

from GameInit import *
from Field import *
from MoveObj import *
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


def StartGame(UniSize, pacman_game, size):
    gameInit = GameInit(size[0] * UniSize, 800)
    
    for y, row in enumerate(pacman_game.numpy_maze):
        for x, column in enumerate(row):
            if column == 0:
                gameInit.AddWall(Wall(gameInit, x, y, UniSize))

    for cookie_space in pacman_game.dotPlace:
        translated = MazeToScreen(cookie_space)
        cookie = Cookie(gameInit, translated[0] + UniSize / 2, translated[1] + UniSize / 2)
        gameInit.AddCookie(cookie)
       
    for powerup_space in pacman_game.powerupSpace:
        translated = MazeToScreen(powerup_space)
        powerup = Powerup(gameInit, translated[0] + UniSize / 2, translated[1] + UniSize / 2)
        gameInit.AddPowerup(powerup)

    for i, ghost_spawn in enumerate(pacman_game.ghost_spawns):
        translated = MazeToScreen(ghost_spawn)
        ghost = Ghost(gameInit, translated[0], translated[1], UniSize, pacman_game, GhostColors[i % 4])
        gameInit.AddGhost(ghost)

    translated = MazeToScreen(pacman_game.hero_spawn)

    pacman = Player(gameInit, translated[0], translated[1], UniSize)
    gameInit.AddPacman(pacman)
    gameInit.isChasing = True
    gameInit.MainLoop(120)

def MainMenu():
    UniSize = 32
    screen_width = 900
    screen_height = 800

    screen=pygame.display.set_mode((screen_width, screen_height))
    white=(255, 255, 255)
    yellow=(255, 255, 50)
    menu=True
    selected="start"
    font = GeneralFont
    def TextFormat(message, textFont, textSize, textColor):
        newFont=pygame.font.Font(textFont, textSize)
        newText=newFont.render(message, 0, textColor)
        return newText
 
    while menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if (selected=="level") & (event.key==pygame.K_UP):
                    selected="start"
                elif (selected=="start") & (event.key==pygame.K_DOWN):
                    selected="level"
                elif (selected=="level") & (event.key==pygame.K_DOWN):
                    selected="quit"
                elif (selected=="quit") & (event.key==pygame.K_UP):
                    selected="level"
                if event.key==pygame.K_RETURN:
                    if selected=="start":
                        pacman_game = MazeAndPathController(diffNormal)
                        size = pacman_game.size
                        StartGame(UniSize, pacman_game, size)
                    if selected=="level":
                        pacman_game = MazeAndPathController(diffEasy)
                        size = pacman_game.size
                        StartGame(UniSize, pacman_game, size)
                    if selected=="quit":
                        pygame.quit()
                        quit()
 
        screen.fill((10, 10, 30))
        title=TextFormat("Pac-Man", font, 60, yellow)
        if selected=="start":
            text_start=TextFormat("START", font, 30, white)
        else:
            text_start = TextFormat("START", font, 30, yellow)

        if selected=="quit":
            text_quit=TextFormat("QUIT", font, 30, white)
        else:
            text_quit = TextFormat("QUIT", font, 30, yellow)

        if selected=="level":
            text_level=TextFormat("LEVEL", font, 30, white)
        else:
            text_level = TextFormat("LEVEL", font, 30, yellow)
 
 
        title_rect=title.get_rect()
        start_rect=text_start.get_rect()
        quit_rect=text_quit.get_rect()
        level_rect=text_level.get_rect()
 
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(text_start, (screen_width/2 - (start_rect[2]/2), 300))
        screen.blit(text_level, (screen_width/2 - (level_rect[2]/2), 360))
        screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 420))
        pygame.display.update()
        pygame.display.set_caption("Pac-Man")

if __name__ == "__main__":
    pygame.init()
    MainMenu()
    
