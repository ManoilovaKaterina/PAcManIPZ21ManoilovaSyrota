import pygame

from GameInit import Direction, ScreenToMaze, MazeToScreen
from MoveObj import MovableObject

class Ghost(MovableObject):
    def __init__(self, surf, x, y, initSize: int, initGameController, SpritePath):
        super().__init__(surf, x, y, initSize)
        self.gameController = initGameController
        self.spritePath = SpritePath
        self.dead = False
        self.movement = True
        self.spawnPoint = [x, y] # початкова координата
        self.spriteBasic = pygame.image.load(SpritePath)
        self.spritePowerup = pygame.image.load("C:/Users/undor/sprites/GhostFright.png")
        
    def ReachedTarget(self): # поведінка при досягненні цілі
        if (self.x, self.y) == self.nextTarget:
            self.nextTarget = self.GetNextLocation()
        self.currentDirection = self.DirectionToNextTarget()

    def SetNewPath(self, path): # задання нового шляху
        for item in path:
            self.locationQueue.append(item)
        self.nextTarget = self.GetNextLocation()
        
    def DirectionToNextTarget(self):
        if self.nextTarget is None: # у режимі переслідування шлях до гравця, інакше - випадковий
            if self.gameInit.isChasing == True and not self.gameInit.IsPowerupActive():
                self.PathToPlayer(self)
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
            self.PathToPlayer(self)
        else:
            self.gameController.NewRanPath(self)
        return Direction.NONE

    def PathToPlayer(self, in_ghost): # знаходження шляху до гравця
        player_position = ScreenToMaze(in_ghost.gameInit.GetPacmanPosition())
        current_maze_coord = ScreenToMaze(in_ghost.getPosition())
        path = self.gameController.p.get_path(current_maze_coord[1], current_maze_coord[0], player_position[1], player_position[0])

        new_path = [MazeToScreen(item) for item in path]
        in_ghost.SetNewPath(new_path)
    
    def tick(self): # зміна кожного кадра
        self.ReachedTarget()
        self.Move(self.currentDirection)

    def Move(self, dir: Direction):
        if(self.movement):
            if dir == Direction.UP:
                self.setPosition(self.x, self.y - 1)
            elif dir == Direction.DOWN:
                self.setPosition(self.x, self.y + 1)
            elif dir == Direction.LEFT:
                self.setPosition(self.x - 1, self.y)
            elif dir == Direction.RIGHT:
                self.setPosition(self.x + 1, self.y)

    def Kill(self):
        self.dead = True
        self.movement = False
        self.setPosition(self.spawnPoint[0], self.spawnPoint[1])

    def draw(self):
        self.image = self.spritePowerup if self.gameInit.IsPowerupActive() else self.spriteBasic
        super(Ghost, self).draw()
