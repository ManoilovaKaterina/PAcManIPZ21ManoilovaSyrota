import pygame

from GameInit import GameInit, Direction, ScreenToMaze, MazeToScreen
from MoveObj import MovableObject

class Ghost(MovableObject):
    def __init__(self: MovableObject, surf: GameInit, x: int, y: int, initSize: int, initGameController, SpritePath: str):
        super().__init__(surf, x, y, initSize)
        self.gameController = initGameController
        self.spritePath = SpritePath
        self.dead = False
        self.movement = True
        self.spawnPoint = [x, y] # початкова координата
        self.spriteBasic = pygame.image.load(SpritePath)
        self.spritePowerup = pygame.image.load("C:/Users/undor/sprites/GhostFright.png")
        
    def ReachedTarget(self: MovableObject): # поведінка при досягненні цілі
        """
        Задає положення наступної цілі та напрямок до неї.
        """
        if (self.x, self.y) == self.nextTarget:
            self.nextTarget = self.GetNextLocation()
        self.currentDirection = self.DirectionToNextTarget()
        
    def DirectionToNextTarget(self: MovableObject) -> Direction:
        """
        Отримує напрямок до наступної цілі.

        :return: напрямок Direction.
        """
        if self.nextTarget is None: # у режимі переслідування шлях до гравця, інакше - випадковий
            if self.gameInit.isChasing == True and not self.gameInit.IsPowerupActive():
                self.PathToPlayer()
            else:
                self.gameController.NewRanPath(self)
            return Direction.NONE

        diff_x = self.nextTarget[0] - self.x
        diff_y = self.nextTarget[1] - self.y
        
        if diff_x == 0: # визначення напряму в залежності від координат
            return Direction.DOWN if diff_y > 0 else Direction.UP
        if diff_y == 0:
            return Direction.LEFT if diff_x < 0 else Direction.RIGHT

        if self.gameInit.isChasing == True and not self.gameInit.IsPowerupActive():
            self.PathToPlayer()
        else:
            self.gameController.NewRanPath(self)
        return Direction.NONE

    def PathToPlayer(self: MovableObject):
        """
        Задає шлях до гравця.
        """
        player_position = ScreenToMaze(self.gameInit.GetPacmanPosition())
        current_maze_coord = ScreenToMaze(self.getPosition())
        path = self.gameController.p.get_path(current_maze_coord[1], current_maze_coord[0], player_position[1], player_position[0])

        new_path = [MazeToScreen(item) for item in path]
        self.SetNewPath(new_path)
    
    def SetNewPath(self: MovableObject, path: list): # задання нового шляху
        """
        Задає новий шлях та наступну ціль привида.
        """
        for item in path:
            self.locationQueue.append(item)
        self.nextTarget = self.GetNextLocation()
        
    def tick(self):
        self.ReachedTarget()
        self.Move(self.currentDirection)

    def Move(self, dir: Direction):
        """
        Рух привида.

        :param dir: напрямок руху.
        """
        if(self.movement):
            if dir == Direction.UP:
                self.setPosition(self.x, self.y - 1)
            elif dir == Direction.DOWN:
                self.setPosition(self.x, self.y + 1)
            elif dir == Direction.LEFT:
                self.setPosition(self.x - 1, self.y)
            elif dir == Direction.RIGHT:
                self.setPosition(self.x + 1, self.y)

    def Kill(self: MovableObject):
        """
        Вбиває привида.
        """
        self.dead = True
        self.movement = False
        self.setPosition(self.spawnPoint[0], self.spawnPoint[1])

    def draw(self: MovableObject):
        self.image = self.spritePowerup if self.gameInit.IsPowerupActive() else self.spriteBasic
        super(Ghost, self).draw()
