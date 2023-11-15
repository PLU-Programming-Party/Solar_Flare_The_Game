import pygame
import random

def backgroundStars():
    allStar = []
    for i in range(250):
        pos1 = random.normalvariate(screen.get_width() / 2, screen.get_width() / 6)
        pos2 = random.normalvariate(screen.get_height() / 2, screen.get_width() / 6)
        starPos = pygame.Vector2(pos1, pos2)
        allStar.append(starPos)
    return allStar

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

wind_position = pygame.Vector2(0, screen.get_height() / 2)

starPos = backgroundStars()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame

    screen.fill("black")
    for star in starPos:
        pygame.draw.circle(screen, "white", star, 1)


    pygame.draw.circle(screen, "yellow", wind_position, 40)

    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_w]:
    #     wind_position.y -= 300 * dt
    # if keys[pygame.K_s]:
    #     wind_position.y += 300 * dt
    # if keys[pygame.K_a]:
    #     wind_position.x -= 300 * dt
    # if keys[pygame.K_d]:
    wind_position.x += 150 * dt

    if(wind_position.x > screen.get_width()):
        wind_position.x = 0
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()



