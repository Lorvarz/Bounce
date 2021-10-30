import pygame


WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

class Target(pygame.sprite.Sprite):

    blockGroup = pygame.sprite.Group() #group all the blocks are in

    def __init__(self, x, y, width, height, WIN):
        """
        :param x: x position of top-left corner
        :param y: y position of top-let corner
        :param width: Width of the block
        :param height: height of the block
        :param WIN: Window block is in
        """
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.surface = pygame.Surface((width, height))
        self.surface.fill(RED)
        self.rect = self.surface.get_rect(center = (x + width//2, y + height//2))
        self.add(Target.blockGroup)
        self.WIN = WIN

    def __str__(self) -> str:
        return f"({self.rect.x}, {self.rect.y})"


    def changeCoordinates(self, *args) -> None:
        """
        Changes the coordinates of the block
        :param args: array containing how much to change them by
        :return: None
        """
        self.x += args[0]
        self.rect.x += args[0]
        if len(args) == 2:
            self.y += args[1]
            self.rect.y += args[1]

    def update(self) -> None:
        """
        Updates the block after each frame
        :return: None
        """
        #draws the block onto its window
        self.WIN.blit(self.surface, (self.x, self.y))
