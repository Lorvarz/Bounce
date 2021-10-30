import pygame
from Target import Target
import random
from Player import Player


#initializes the text fonts
pygame.font.init()
scorefont = pygame.font.SysFont("comicsans", 30)
winFont = pygame.font.SysFont("comicsans", 70)

#makes and names the window
WIDTH, HEIGHT = 1000,618
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bounce!")



#defines some colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

#defines the FPS
FPS = 60

def drawWindow() -> None:
    """
    Draws all the objects onto the window
    :return: None
    """
    WIN.fill(WHITE) #fills background with White

    #update both blcks and player
    Player.playerGroup.update()
    Target.blockGroup.update()


    #Checks if game is over and acts accordingly
    if len(Target.blockGroup.sprites()) == 0:
        winText = winFont.render(f"YOU WIN!", True, (0, 0, 0))
        WIN.blit(winText, (400, 200))

        scoreText = scorefont.render(f"Score: {Player.playerGroup.sprites()[0].score}", True, (0, 0, 0))
        WIN.blit(scoreText, (450, 300))

    #writes down the score
    else:
        scoreText = scorefont.render(f"Score: {Player.playerGroup.sprites()[0].score}", True, (0, 0, 0))
        WIN.blit(scoreText, (10, 10))


    pygame.display.update()#draws the window with all the new changes

def mainLoop() -> None:
    """
    Runs the loop of the game
    :return: None
    """

    #removes all the items from the groups
    Player.playerGroup.empty()
    Target.blockGroup.empty()


    #----------------- Make Targets -----------
    howMany = 50
    width, height = (10, 10)
    for i in range(howMany):
        x = random.randint(0, WIDTH - width)
        y = random.randint(0, HEIGHT - height - 100)
        Target(x, y, width, height, WIN)

    # ----------------- Make players -----------
    howMany = 1
    for i in range(howMany):
        x = random.randint(0, WIDTH - 8)
        y = HEIGHT - 8
        Player(x, y, WIN)


    clock = pygame.time.Clock() #creates clock to regulate FPS

    WIN.fill(WHITE)

    run = True
    draw = True #whether to draw the window or not
    while run: #Game loop
        clock.tick(FPS) #checks the FPS

        #------------------ EVENTS ----------------------

        for event in pygame.event.get():

            # checks to quit the game
            if event.type == pygame.QUIT:
                run = False

        #------------------ MOUSE EVENTS ----------------

            #handles the player clicking
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for player in Player.playerGroup.sprites():
                        player.setVector(pygame.mouse.get_pos())
                        #player.setVector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])



        #------------------ KEY EVENTS ------------------
            if event.type == pygame.KEYDOWN:

                #draws 1 frame
                if event.key == pygame.K_LSHIFT:
                    drawWindow()

                #restarts the game
                if event.key == pygame.K_RSHIFT:
                    mainLoop()

                #stops game time
                if event.key == pygame.K_SPACE:
                    draw = not draw


                #----------- Super Secret Cheat Codes --------

                #Makes more player instances
                if event.key == pygame.K_m:
                    x = random.randint(0, WIDTH - 8)
                    y = random.randint(0, HEIGHT - 8)
                    Player(x, y, WIN)

                #Makes all player bigger
                if event.key == pygame.K_UP:
                    for player in Player.playerGroup.sprites():
                        player.changeRadius(1)

                #Makes all players smaller
                if event.key == pygame.K_DOWN:
                    for player in Player.playerGroup.sprites():
                        player.changeRadius(-1)

                #Makes all players faster
                if event.key == pygame.K_RIGHT:
                    for player in Player.playerGroup.sprites():
                        player.baseSpeed += 1
                    print(player.baseSpeed)

                #Makes all players smaller
                if event.key == pygame.K_LEFT:
                    for player in Player.playerGroup.sprites():
                        player.baseSpeed -= 1
                    print(player.baseSpeed)

                #Makes the players jump even if they used their jump
                if event.key == pygame.K_h:
                    for player in Player.playerGroup.sprites():
                        for player in Player.playerGroup.sprites():
                            player.setVector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

                #Creates more blocks
                if event.key == pygame.K_l:
                    howMany = 100
                    width, height = (10, 10)
                    for i in range(howMany):
                        x = random.randint(0, WIDTH - width)
                        y = random.randint(0, HEIGHT - height)
                        Target(x, y, width, height, WIN)



        if draw:
            drawWindow()

    pygame.quit()#quits the game


if __name__ == '__main__':
    mainLoop()