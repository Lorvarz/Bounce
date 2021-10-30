import pygame
import pygame.math as pymath
from Target import Target
from multipledispatch import dispatch
from math import copysign
from math import log

aquaGreen = (0,192,163)

class Player(pygame.sprite.Sprite):

    playerGroup = pygame.sprite.Group() # group the players are in

    def __init__(self, x, y, WIN):
        """
        :param x: x position of top-left corner
        :param y: y position of top-left corner
        :param WIN: Window the player is in
        """
        pygame.sprite.Sprite.__init__(self)
        self.surface = pygame.Surface((8, 8))
        self.radius = 5
        self.rect = pygame.Rect(x - self.radius, y - self.radius, 2*self.radius, 2*self.radius)
        self.add(Player.playerGroup)
        self.baseSpeed = 10
        self.currentSpeed = self.baseSpeed
        self.vector = pymath.Vector2(0,1)
        self.vector.scale_to_length(self.baseSpeed)
        self.jump = True
        self.WIN = WIN
        self.score = 0
        self.streak = 0

    def __str__(self):
        return f"({self.rect.x}, {self.rect.y})"


    # --------------- MOVEMENT ---------------
    # Note: in pygame the positive Y direction is down, and the negative is up

    def changeCoordinates(self, x, y, draw) -> None:
        """
        Takes in by how much to change the x and y coordinates and wether or
            not to draw itself on the window
        :param x: change in x position
        :param y: change in y position
        :param draw: whether to draw or not
        :return: None
        """

        self.rect.x += x

        #checks if the player will go below the bottom of the screen
        if self.rect.y + y + 2*self.radius < self.WIN.get_height() and self.vector.y != 0:
            self.rect.y += y
        else:
            self.rect.y = self.WIN.get_height() - (2*self.radius) - 1
            self.vector.y = 0
            self.streak = 0
            self.friction(0.3)
            self.currentSpeed = self.baseSpeed
            self.jump = True

        #Draws the player on the window
        if draw: pygame.draw.circle(self.WIN, aquaGreen, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)



    # --------------- VECTORS ---------------

    @dispatch(int, int)
    def setVector(self, x, y) -> None:
        """
        sets the speed vector of the player towards the given coordinates
            No need for player to have its jump
        :param x: x coordinate to point to
        :param y: y coordinate to point to
        :return: None
        """
        if x == 0 and y == 0:
            self.vector.x = 0
            self.vector.y = 0
        else:
            self.vector.x = x - (self.rect.x + self.radius)
            self.vector.y = y - (self.rect.y + self.radius)
            self.vector.scale_to_length(self.currentSpeed)
            self.jump = False

    @dispatch((tuple))
    def setVector(self, pos) -> None:
        """
        Lauches the player towards a given coordinate
            only if player has its jump
        :param pos: tuple representing coordinates of where to point
        :return: None
        """
        if self.jump:
            self.vector.x = pos[0] - (self.rect.x + self.radius)
            self.vector.y = pos[1] - (self.rect.y + self.radius)

            self.vector.scale_to_length(self.currentSpeed)
            self.jump = False

    def changeYVector(self, magnitude) -> None:
        """
        Changed the Y-component of the player's velocity vector by a
            given amount
        :param magnitude: how much to change the vector by
        :return: None
        """
        self.vector.y += magnitude

    def changeXVector(self, magnitude) -> None:
        """
        Changed the X-component of the player's velocity vector by a
            given amount
        :param magnitude: how much to change the vector by
        :return: None
        """
        self.vector.x += magnitude


    # --------------- COLLISIONS ---------------

    def checkCollisions(self) -> None:
        """
        Handles the player's collisions with blocks
        :return: None
        """
        #checks if player is colliding with a block
        collisions = pygame.sprite.spritecollide(self, Target.blockGroup, True)

        if collisions:

            self.bounce(True, True, 1.1) #makes player bounce and speed up
            self.jump = True
            self.streak += 1
            self.score += 100 + int(100*log(self.streak) * (0.2)) #awards points based on streak


    def checkSides(self) -> None:
        """
        Handles player's collisions with the sides of the screen
        :return: None
        """
        bounceAcceleration = 0.8 #how much to slow down or speed up the player by
                                 # > 1 will speed up, < 1 will slow down

        #checks collision with left side
        if self.rect.x + self.vector.x < 0:
            # find distance to side
            toMarginX = self.rect.x
            slope = self.vector.y / self.vector.x
            toMarginY = toMarginX * slope

            # moves and makes the player bounce
            self.changeCoordinates(toMarginX, toMarginY, False)
            self.changeCoordinates(-(self.vector.x - toMarginX), self.vector.y - toMarginY, False)
            self.bounce(True, False, bounceAcceleration)


        #checks collision with right side
        if self.rect.x + (self.radius * 2) + self.vector.x >= self.WIN.get_width():
            # find distance to side
            toMarginX = self.WIN.get_width() - (self.rect.x + (self.radius * 2))
            slope = self.vector.y / self.vector.x
            toMarginY = toMarginX * slope

            # moves and makes the player bounce
            self.changeCoordinates(toMarginX, toMarginY, False)
            self.changeCoordinates(-(self.vector.x - toMarginX), self.vector.y - toMarginY, False)
            self.bounce(True, False, bounceAcceleration)


    # --------------- PHYSICS ---------------
    def gravity(self) -> None:
        """
        Exerts the force of gravity on the player
        :return: None
        """
        #will only exert it if the player is in free fall and below terminal velocity
        if self.rect.y != self.WIN.get_height() - (2*self.radius) - 1:
            if self.vector.y < 9:
                #if above the screen it falls faster
                if self.rect.y > self.WIN.get_height():
                    self.changeYVector(0.11)
                else:
                    self.changeYVector(0.08)


    def friction(self, magnitude) -> None:
        """
        Exerts a force of friction
        :param force: Magnitude of the force
        :return: None
        """
        # Stops the player
        if abs(self.vector.x) < magnitude:
            self.vector.x = 0
            self.vector.y = 0
        #slows down the player
        else:
            force = - (copysign(magnitude, self.vector.x))
            self.changeXVector(force)

    def bounce(self, x, y, acceleration) -> None:
        """
        Makes the player bounce by flippling the x and/or y components of the
            velocity vector. Multiplies its magnitude by the acceleration
        :param x: whether to flip x or not
        :param y: whether to flip y or not
        :param acceleration: multiplier for the velocity
        :return: None
        """
        if x: self.vector.x = -self.vector.x
        if y: self.vector.y = -self.vector.y

        self.currentSpeed *= acceleration

        self.vector.scale_to_length(self.currentSpeed)

    # --------------- PARAMETERS ---------------
    def changeRadius(self, change) -> None:
        """
        Alters the radius of the player by the change value
        :param change: how much to change the radius by
        :return: None
        """
        self.radius += change
        #redraws the circle based on new radius
        self.rect = pygame.Rect(self.rect.x, self.rect.y, 2 * self.radius, 2 * self.radius)
        self.changeCoordinates(0, -1, False)

    def maxHeight(self) -> None:
        """
        If the player is too high in the sky, brings it back down
        :return: None
        """
        if self.rect.y > 1.2 * self.WIN.get_height():
            self.rect.y = -self.radius * 2
            if self.vector.y > 0:
                self.vector.y = 9


    # --------------- UPDATE ---------------

    def update(self) -> None:
        """
        Updates the player after each frame
        :return: None
        """

        self.gravity()
        length = self.vector.length()

        self.maxHeight()

        #if the velocity of the player is higher than the width of the blocks
        # it splits that velocity in chucks so it doesn't teleport over them
        copy = pymath.Vector2(self.vector)
        while length >= 10:

            copy.scale_to_length(10)

            initial = self.vector.length()
            self.changeCoordinates(copy.x, copy.y, (length == 10))
            self.checkCollisions()
            self.checkSides()

            length += self.vector.length() - initial
            length -= 10

        if length > 0:
            copy = pymath.Vector2(self.vector)
            copy.scale_to_length(length)



        self.changeCoordinates(copy.x, copy.y, True)
        self.checkCollisions()
        self.checkSides()







