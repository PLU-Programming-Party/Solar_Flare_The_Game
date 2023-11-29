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
                player.velocity = pygame.Vector2(player.velocity.x + (particle.velocity.x * scalar), player.velocity.y + (particle.velocity.y * scalar))
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
    def __init__(self, position, velocity, size, image):
        self.position = position
        self.velocity = velocity
        self.size = size
        self.image = image

    def tick(self, screen, dt):
        self.velocity = self.velocity + pygame.Vector2(0, 30) * dt
        self.position = self.position + self.velocity * dt
        if (self.position.x > screen.get_width()):
            self.position.x = screen.get_width()

        if (self.position.x < 0):
            self.position.x = 0

        # pygame.draw.circle(screen, "green", self.position, self.size)
        screen.blit(self.image, self.position)



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

spaceman = pygame.image.load('img.png')
player = Player(pygame.Vector2(screen.get_width() / 2, 0), pygame.Vector2(0, 150), 15, spaceman)
particleSpitter = ParticleManagerSpitter(pygame.Vector2(screen.get_width() / 2, screen.get_height()))

starPos = backgroundStars()


while running:
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if player.position.y < 0 or player.position.y > screen.get_height():
        pygame.font.init()
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = my_font.render('Game Over You Win?', False, (255, 255, 255))
        play_again = my_font.render('hold SPACE to play again', False, (255, 255, 255))
        screen.blit(text_surface, (screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(play_again, (screen.get_width() / 2, screen.get_height() / 2 + 40))
        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.position = pygame.Vector2(screen.get_width() / 2, 1)
            player.velocity = pygame.Vector2(0, 150)
            particleSpitter.particleArray = []

        continue



    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    for star in starPos:
        pygame.draw.circle(screen, "white", star, 1)

    particleSpitter.spit(screen, dt, player)
    player.tick(screen, dt)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.velocity = player.velocity + pygame.Vector2(-5, 0)
    if keys[pygame.K_d]:
        player.velocity = player.velocity + pygame.Vector2(5, 0)

    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()




