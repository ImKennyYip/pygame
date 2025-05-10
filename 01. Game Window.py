import pygame
from sys import exit #terminate the program

#game variables
GAME_WIDTH = 512
GAME_HEIGHT = 512

pygame.init() #always needed to initialize pygame
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Kenny Yip Coding - Pygame") #title of the window
clock = pygame.time.Clock() #used for the frame rate

while True: #game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #user clicks the X button in window
            pygame.quit()
            exit()
    
    pygame.display.update()
    clock.tick(60) #60 frames per second (fps)
