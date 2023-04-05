import pygame

from GameInit import GameInit, MazeToScreen, GeneralFont
from Field import MazeAndPathController, diffEasy, diffHard, diffNormal
from Ghost import Ghost
from Player import Player
from StaticObjects import Wall, NoPlayerSpace, Cookie, Powerup

NameFont = 'text/8_bit_arcade/8-bit Arcade Out.ttf'
NameFontIn = 'text/8_bit_arcade/8-bit Arcade In.ttf'

GhostColors = [
            "images/RedGhost.png",
            "images/PinkGhost.png",
            "images/OrangeGhost.png",
            "images/BlueGhost.png"
        ]


def StartGame(UniSize: int, pacman_game: MazeAndPathController, size: int):
    """
    Задає параметри та починає гру.

    :param UniSize: параметр масштабування гри.
    :param pacman_game: поле гри.
    :param size: розмір вікна.
    """
    gameInit = GameInit(size[0] * UniSize, 800)

    for y, row in enumerate(pacman_game.numpy_maze):
        for x, column in enumerate(row):
            if column == 0:
                gameInit.AddWall(Wall(gameInit, x, y, UniSize))

    for no_player_space in pacman_game.noPlayerSpaces:
        translated = no_player_space
        new_nps = NoPlayerSpace(gameInit, translated[0],
                                translated[1], UniSize)
        gameInit.AddNPS(new_nps)

    for cookie_space in pacman_game.dotPlace:
        translated = MazeToScreen(cookie_space)
        cookie = Cookie(gameInit, translated[0] + UniSize/2,
                        translated[1] + UniSize/2)
        gameInit.AddCookie(cookie)

    for powerup_space in pacman_game.powerupSpace:
        translated = MazeToScreen(powerup_space)
        powerup = Powerup(gameInit, translated[0] + UniSize/2,
                          translated[1] + UniSize/2)
        gameInit.AddPowerup(powerup)

    for i, ghost_spawn in enumerate(pacman_game.ghost_spawns):
        translated = MazeToScreen(ghost_spawn)
        ghost = Ghost(gameInit, translated[0], translated[1],
                      UniSize, pacman_game, GhostColors[i % 4])
        gameInit.AddGhost(ghost)

    translated = MazeToScreen(pacman_game.hero_spawn)

    pacman = Player(gameInit, translated[0], translated[1], UniSize)
    gameInit.AddPacman(pacman)
    gameInit.isChasing = True
    gameInit.MainLoop(120)


def MainMenu():
    """ Головне меню гри."""
    UniSize = 32
    screen_width = 900
    screen_height = 800

    screen = pygame.display.set_mode((screen_width, screen_height))
    white = (255, 255, 255)
    yellow = (255, 209, 102)
    menu = True
    selected = "start"
    font = GeneralFont

    def TextFormat(message, textFont, textSize, textColor):
        newFont = pygame.font.Font(textFont, textSize)
        newText = newFont.render(message, 0, textColor)
        return newText

    def ImageFormat(img):
        imgf = pygame.transform.scale(pygame.image.load(img), (60, 60))
        return imgf
    Choose = "menu"

    while menu:
        screen.fill((1, 14, 18))
        screen.blit(ImageFormat(GhostColors[0]), (5, 5))
        screen.blit(ImageFormat(GhostColors[1]), (screen_width-65, 5))
        screen.blit(ImageFormat(GhostColors[2]), (5, screen_height-110))
        screen.blit(ImageFormat(GhostColors[3]),
                    (screen_width-65, screen_height-110))
        titleIn = TextFormat("Pac Man", NameFontIn, 120, yellow)
        title = TextFormat("Pac Man", NameFont, 120, (15, 100, 200))
        titleIn_rect = titleIn.get_rect()
        title_rect = title.get_rect()

        screen.blit(titleIn, (screen_width/2 - (titleIn_rect[2]/2), 80))
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        if Choose == "menu":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                    if ((selected == "rules") and
                        ((event.key == pygame.K_UP) or
                         (event.key == pygame.K_w))):
                        selected = "start"
                    elif ((selected == "start") and
                          ((event.key == pygame.K_DOWN) or
                           (event.key == pygame.K_s))):
                        selected = "rules"
                    elif ((selected == "rules") and
                          ((event.key == pygame.K_DOWN) or
                           (event.key == pygame.K_s))):
                        selected = "quit"
                    elif ((selected == "quit") and
                          ((event.key == pygame.K_UP) or
                           (event.key == pygame.K_w))):
                        selected = "rules"
                    if event.key == pygame.K_RETURN:
                        if selected == "start":
                            selected = "easy"
                            Choose = "diff"
                        if selected == "rules":
                            Choose = "rules"
                        if selected == "quit":
                            pygame.quit()
                            quit()

            if selected == "start":
                text_start = TextFormat("START", font, 30, white)
            else:
                text_start = TextFormat("START", font, 30, yellow)

            if selected == "quit":
                text_quit = TextFormat("QUIT", font, 30, white)
            else:
                text_quit = TextFormat("QUIT", font, 30, yellow)

            if selected == "rules":
                text_level = TextFormat("RULES", font, 30, white)
            else:
                text_level = TextFormat("RULES", font, 30, yellow)
            start_rect = text_start.get_rect()
            quit_rect = text_quit.get_rect()
            level_rect = text_level.get_rect()
            screen.blit(text_start, (screen_width/2 - (start_rect[2]/2), 320))
            screen.blit(text_level, (screen_width/2 - (level_rect[2]/2), 380))
            screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 440))
        elif Choose == "diff":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        selected = "start"
                        Choose = "menu"
                    if ((selected == "normal") and
                        ((event.key == pygame.K_UP) or
                         (event.key == pygame.K_w))):
                        selected = "easy"
                    elif ((selected == "easy") and
                          ((event.key == pygame.K_DOWN) or
                           (event.key == pygame.K_s))):
                        selected = "normal"
                    elif ((selected == "normal") and
                          ((event.key == pygame.K_DOWN) or
                           (event.key == pygame.K_s))):
                        selected = "hard"
                    elif ((selected == "hard") and
                          ((event.key == pygame.K_UP) or
                           (event.key == pygame.K_w))):
                        selected = "normal"
                    if event.key == pygame.K_RETURN:
                        if selected == "easy":
                            pacman_game = MazeAndPathController(diffEasy)
                            size = pacman_game.size
                            StartGame(UniSize, pacman_game, size)
                        if selected == "normal":
                            pacman_game = MazeAndPathController(diffNormal)
                            size = pacman_game.size
                            StartGame(UniSize, pacman_game, size)
                        if selected == "hard":
                            pacman_game = MazeAndPathController(diffHard)
                            size = pacman_game.size
                            StartGame(UniSize, pacman_game, size)

            if selected == "easy":
                text_easy = TextFormat("EASY", font, 30, white)
            else:
                text_easy = TextFormat("EASY", font, 30, yellow)

            if selected == "normal":
                text_norm = TextFormat("NORMAL", font, 30, white)
            else:
                text_norm = TextFormat("NORMAL", font, 30, yellow)

            if selected == "hard":
                text_hard = TextFormat("HARD", font, 30, white)
            else:
                text_hard = TextFormat("HARD", font, 30, yellow)
            easy_rect = text_easy.get_rect()
            normal_rect = text_norm.get_rect()
            hard_rect = text_hard.get_rect()
            screen.blit(text_easy, (screen_width/2 - (easy_rect[2]/2), 320))
            screen.blit(text_norm, (screen_width/2 - (normal_rect[2]/2), 380))
            screen.blit(text_hard, (screen_width/2 - (hard_rect[2]/2), 440))
        elif Choose == "rules":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        selected = "start"
                        Choose = "menu"

            with open('text/rules.txt', 'r') as file:
                data = file.read().split("\n")
            i = 0
            for d in data:
                text = TextFormat(d, font, 16, yellow)
                text_rect = text.get_rect()
                screen.blit(text, (screen_width/2 - (text_rect[2]/2), 250+i))
                i += 25

        pygame.display.update()
        pygame.display.set_caption("Pac-Man")


if __name__ == "__main__":
    pygame.init()
    MainMenu()
