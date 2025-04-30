import pygame

# initialise the game
pygame.init()

# set the window dimensions
width = 800
height = 600

# create the window
screen = pygame.display.set_mode((width, height))

# set the window title
pygame.display.set_caption('Asteroids')

# game loop
running = True
while running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # clear the screen
    screen.fill((0, 0, 0))

    # update the display
    pygame.display.flip()

# quit pygame
pygame.quit()