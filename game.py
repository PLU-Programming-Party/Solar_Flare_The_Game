import math

import pygame
import random


class Particle:
    def __init__(self, position, size, velocity):
        self.position = position
        self.size = size
        self.velocity = velocity
        #chai tea, chai means tea, you are saying tea tea bro.


class ParticleManagerSpitter():
    #80mphMonster
    #GarbageIsGood
    def __init__(self, position):
        self.particleArray = []
        self.position = position
        self.rotation = 360

    def spit(self, screen, dt, player):
        velocityVector = pygame.Vector2(150,0)
        self.rotation = random.randint(-180, 0)
        self.particleArray.append(Particle(self.position.copy(), random.uniform(2,8), velocityVector.rotate(self.rotation)))
        for particle in self.particleArray:
            particle.position += particle.velocity * dt
            if (collisionDetector(player, particle)):
                particle.position.y = screen.get_width() + 1
                scalar = (particle.size/player.size)
                player.velocity = pygame.Vector2((player.velocity.x + particle.velocity.x) * scalar, (player.velocity.y + particle.velocity.y) * scalar)
        self.spitoon(screen)
        for particle in self.particleArray:
            pygame.draw.circle(screen, "orange", particle.position, particle.size)



    def spitoon(self, screen):
        #spitoon
        self.particleArray = [p for p in self.particleArray if not self.spitoonable(screen, p)]



    def spitoonable(self, screen, p):
        if ((p.position.x > screen.get_width()) or (p.position.x < 0) or (p.position.y > screen.get_height()) or (p.position.y < 0)):
            return True
        else:
            return False

class Player:
    def __init__(self, position, velocity, size):
        self.position = position
        self.velocity = velocity
        self.size = size

    def tick(self, screen, dt):
        pygame.draw.circle(screen, "green", self.position, self.size)
        self.position = self.position + self.velocity * dt
        if (self.position.x > screen.get_width()):
            self.position.x = 0



def backgroundStars():
    allStar = []
    for i in range(250):
        pos1 = random.normalvariate(screen.get_width() / 2, screen.get_width() / 6)
        pos2 = random.normalvariate(screen.get_height() / 2, screen.get_width() / 6)
        starPos = pygame.Vector2(pos1, pos2)
        allStar.append(starPos)
    return allStar


def collisionDetector(player, particle):
    dist = math.sqrt((player.position.x - particle.position.x) ** 2 + (player.position.y - particle.position.y) ** 2)
    return (dist <= (particle.size + player.size))



# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player = Player(pygame.Vector2(0, screen.get_height() / 2), pygame.Vector2(150, 0), 15)
particleSpitter = ParticleManagerSpitter(pygame.Vector2(screen.get_width() / 2, screen.get_height()))

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

    particleSpitter.spit(screen, dt, player)
    player.tick(screen, dt)

    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_w]:
    #     wind_position.y -= 300 * dt
    # if keys[pygame.K_s]:
    #     wind_position.y += 300 * dt
    # if keys[pygame.K_a]:
    #     wind_position.x -= 300 * dt
    # if keys[pygame.K_d]:
    #     wind_position.x += 150 * dt
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()




