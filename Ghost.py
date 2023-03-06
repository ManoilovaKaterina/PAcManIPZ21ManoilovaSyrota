import pygame

from GameInit import Direction, ScreenToMaze, MazeToScreen
from MoveObj import MovableObject

class Ghost(MovableObject):
    def __init__(self, surf, x, y, initSize: int, initGameController, SpritePath):
        super().__init__(surf, x, y, initSize)
        self.gameController = initGameController
        self.spriteBasic = pygame.image.load(SpritePath)
        
    def ReachedTarget(self): # поведінка при досягненні цілі
        if (self.x, self.y) == self.nextTarget:
            self.nextTarget = self.GetNextLocation()
        self.currentDirection = self.DirectionToNextTarget()

    def SetNewPath(self, path): # задання нового шляху
        for item in path:
            self.locationQueue.append(item)
        self.nextTarget = self.GetNextLocation()
        
    def DirectionToNextTarget(self):
        if self.nextTarget is None:
            self.gameController.NewRanPath(self)
            return Direction.NONE
        diff_x = self.nextTarget[0] - self.x
        diff_y = self.nextTarget[1] - self.y
        if diff_x == 0:
            return Direction.DOWN if diff_y > 0 else Direction.UP
        if diff_y == 0:
            return Direction.LEFT if diff_x < 0 else Direction.RIGHT
        self.gameController.NewRanPath(self)
        return Direction.NONE
    
    def tick(self): # зміна кожного кадра
        self.ReachedTarget()
        self.Move(self.currentDirection)

    def Move(self, dir: Direction):
        if dir == Direction.UP:
            self.setPosition(self.x, self.y - 1)
        elif dir == Direction.DOWN:
            self.setPosition(self.x, self.y + 1)
        elif dir == Direction.LEFT:
            self.setPosition(self.x - 1, self.y)
        elif dir == Direction.RIGHT:
            self.setPosition(self.x + 1, self.y)

    def draw(self):
        self.image = self.spriteBasic
        super(Ghost, self).draw()
